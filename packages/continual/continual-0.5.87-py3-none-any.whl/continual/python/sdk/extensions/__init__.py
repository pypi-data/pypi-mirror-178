from __future__ import annotations
import yaml
import toml
import os
import shutil
from pathlib import Path
from typing import Optional, List, Tuple
import subprocess
from glob import glob
import requests
import hashlib
import sys
import tarfile

from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.events import EventManager
from continual.python.sdk.extensions import templates


TEMPLATES_DIR_PATH = os.path.dirname(templates.__file__)
DEFAULT_TEMPLATE_CLASS_BY_TYPE = {
    "algorithm": "MyCustomAlgorithm",
    "model": "MyModelPipeline",
}


class ExtensionManager(Manager):
    """Manages promotion resources."""

    name_pattern: str = "projects/{project}/extensions/{extension}"

    def get(self, id: str) -> Extension:
        """
        Get extension

        Parameters
        ----------
        id: str
            Extension id

        Returns
        -------
        An extension
        """
        req = management_pb2.GetExtensionRequest(name=self.name(id))
        resp = self.client._management.GetExtension(req)
        return Extension.from_proto(resp, client=self.client)

    def list(
        self,
        page_size: Optional[int] = None,
        all_projects: bool = False,
    ) -> List[Extension]:
        """
        List extensions

        Parameters
        ---------
        page_size: int
            Number of items to return
        all_projects: bool
            Whether to show all projects or not
        """

        req = management_pb2.ListExtensionsRequest(
            parent=self.parent,
            page_size=page_size,
            all_projects=all_projects,
        )
        resp = self.client._management.ListExtensions(req)
        return [Extension.from_proto(x, client=self.client) for x in resp.extensions]

    def delete(self, id: str):
        """
        Delete an extension

        Parameters
        ----------
        id : str
            Name of the extension to delete
        """

        req = management_pb2.DeleteExtensionRequest(name=self.name(id))
        self.client._management.DeleteExtension(req)

    def export(self, id: str, path: Path, extract: bool) -> str:
        """
        Get the source code tarball
        for this extension and possibly untar
        it

        Parameters
        ----------
        id : str
            Name of the extension
        path: Path
            Path to which to download the source tarball
        extract: bool
            Whether or not to extract the contents of the
            tarball

        Returns
        -------
        str
            Path to exported file/directory
        """

        req = management_pb2.ExportExtensionRequest(name=self.name(id))
        signed_url = self.client._management.ExportExtension(req)

        res = requests.get(signed_url.signed_url, stream=True)
        new_file_path = os.path.join(path, f"{id}.tar.gz")
        with open(new_file_path, "wb") as f:
            f.write(res.content)
        if extract:
            with tarfile.open(name=new_file_path, mode="r") as f:
                old_file_path = new_file_path
                new_file_path = os.path.join(path, id)
                f.extractall(new_file_path)
            os.remove(old_file_path)
        return new_file_path

    def install(self, id: str):
        """
        Pip install extension python package using straight from signed URL

        Parameters
        ----------
        id : str
            Name of the extension

        """

        req = management_pb2.ExportExtensionRequest(name=self.name(id))
        signed_url = self.client._management.ExportExtension(req)

        # Uninstall older version of extension if any
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "uninstall",
                    "-y",
                    id.lower(),
                ],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            raise Exception(
                f"Could not uninstall older version of extension {id} : {str(e.output, encoding='utf-8')}, {str(e.stderr, encoding='utf-8')}, {str(e.stdout, encoding='utf-8')}"
            )

        # Now install it
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    signed_url.signed_url,
                ],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            raise Exception(
                f"Could not install extension {id} : {str(e.output, encoding='utf-8')}, {str(e.stderr, encoding='utf-8')}, {str(e.stdout, encoding='utf-8')}"
            )

    def init(
        self,
        root: str,
        id: str,
        extension_type: str,
        class_name: str,
        source_path: str,
        dependencies: List[str],
    ):
        """
        Creates a template pip-managed python project for a Continual Extension
        with given parameters

        Parameters
        ----------
        root: str
            Absolute path to directory in which to create the project
        id: str
            ID of the extension, used in other resource YAMLs to identify extension
        extension_type: str
            Type of the extension. Must be one of the supported types
        class_name: str
            The name of the class that will contain the model implementation
        source_path: str
            The optional path to the source file implementation to copy into the directory,
            if not specified a template implementation will be copied into the extension directory
        dependencies: List[str]
            Names of pip package dependencies (with versions attached) to be passed to poetry add
        """

        ext_dir = os.path.join(root, id)

        # Run poetry new
        try:
            # Create the directory
            subprocess.run(
                ["poetry", "new", id, "--name", id],
                check=True,
                capture_output=True,
                cwd=root,
            )
        except subprocess.CalledProcessError as e:
            raise Exception(
                f"Could not create new package {id} : {str(e.output, encoding='utf-8')}"
            )

        # Add package dependencies to project file if any
        if dependencies:
            try:
                subprocess.run(
                    ["poetry", "add", "--lock"] + dependencies,
                    check=True,
                    capture_output=True,
                    cwd=ext_dir,
                )
            except subprocess.CalledProcessError as e:
                raise Exception(
                    f"Could not add package dependencies for {id} : {str(e.output, encoding='utf-8')}"
                )

        self._copy_template(root, id, extension_type, source_path, class_name)
        self._add_extension_schema(root, id, class_name, extension_type)

    def _copy_template(
        self,
        root: str,
        extension_id: str,
        extension_type: str,
        source_path: str,
        class_name: str,
    ):
        """
        Create a template in the extension  python package to faciliate dev
        """

        ext_dir = os.path.join(root, extension_id)

        # The name needs to be lowercase here because of the way poetry creates directories
        dest_file_path = os.path.join(
            ext_dir, extension_id.lower(), f"{extension_type}.py"
        )
        if not source_path:
            src_file_path = os.path.join(
                TEMPLATES_DIR_PATH, f"template_custom_{extension_type}.py"
            )
            with open(src_file_path, "r") as fin, open(dest_file_path, "w+") as fout:
                template_contents = fin.read()
                if class_name:
                    template_contents = template_contents.replace(
                        DEFAULT_TEMPLATE_CLASS_BY_TYPE[extension_type],
                        class_name,
                    )
                fout.write(template_contents)
                fout.flush()
                os.fsync(fout)
        else:
            # Copy over existing implementation file
            shutil.copy(source_path, dest_file_path)

    def _add_extension_schema(
        self, root: str, extension_id: str, class_name: str, extension_type: str
    ):
        """
        Create an extension yaml for a custom extension at path

        Parameters
        ----------
        path: str
            The root directory of the extension source tree
        extension_id: str
            The name/label for the extension
        class_name: str
            The name of the extension implementation
        """

        schema = {
            "type": "extension",
            "extension_type": extension_type,
            "extension_id": extension_id,
            "module_name": ".".join([extension_id.lower(), extension_type]),
            "class_name": class_name
            if class_name
            else DEFAULT_TEMPLATE_CLASS_BY_TYPE[extension_type],
        }

        with open(os.path.join(root, extension_id, "extension.yaml"), "w") as f:
            yaml.dump(schema, f)

    def push_extension(self, root: str, schema: dict) -> dict:
        """
        Prepare package and upload into continual

        Parameters
        ----------
        root: str
            the path to the package root directory
        schema: dict
            yaml config/schema for the extension rooted at
            root.e
        """

        new_schema = schema.copy()

        # Get the full resource name
        new_schema["name"] = self.name(schema["extension_id"])

        # Package if necessary, and attach package md5 and resource_url to schema
        package_path = self._package_extension(root=root, schema=new_schema)
        new_schema["package_hash"] = self._create_package_hash(
            package_path=package_path
        )
        signed_url, new_schema["package_url"] = self._get_extension_bucket_info(
            extension_id=schema["extension_id"],
            package_filename=Path(package_path).name,
        )

        # Upload file
        resp = requests.put(
            url=signed_url,
            data=open(package_path, "rb").read(),
            headers={"Content-Type": "application/gzip"},
        )
        if resp.text != "":
            raise Exception(
                f"Could not upload package {package_path} to Continual: {resp.text}"
            )
        return new_schema

    def _package_extension(self, root: str, schema: dict) -> str:
        """
        Packages a particular extension given the yaml

        Parameters
        ----------
        root: str
            the path to the package root directory
        schema: dict
            yaml config/schema for the extension rooted at
            root.

        Returns
        -------
        str
            absolute path to distributable package file

        Raises
        ------
        Exception
            If packaging process failed
        """

        # If the package-path is not specified, run the default package manager
        if not "package_path" in schema:
            # Add YAMLs to package data
            try:
                pyproject_filepath = os.path.join(root, "pyproject.toml")
                pyproject_file = toml.load(pyproject_filepath)
                pyproject_file["tool"]["poetry"]["include"] = ["*.yaml"]
                with open(pyproject_filepath, "w") as f:
                    toml.dump(pyproject_file, f)
            except Exception as e:
                raise Exception(
                    f"pyproject file could not be edited to include package data: {e}"
                )
            # poetry build
            try:
                subprocess.run(
                    ["poetry", "build"], check=True, capture_output=True, cwd=root
                )
            except subprocess.CalledProcessError as e:
                raise Exception(
                    f"Could not build package '{schema['name']}' for push: {str(e.output, encoding='utf-8')}"
                )

            dist_packages = glob(os.path.join(root, "dist", "*.tar.gz"))
            if len(dist_packages) != 1:
                raise Exception(
                    f"Package build failed. Remove old .tar.gz files from {os.path.join(root, 'dist')}"
                )
            else:
                package_path = dist_packages[0]
        else:
            package_path = schema["package_path"]

        return package_path

    def _create_package_hash(self, package_path: str) -> str:
        """
        Creates an md5 hash of contents of distributable
        package file

        Parameters
        ----------
        package_path: str
            absolute path to distributable package file

        Returns
        -------
        str
            md5 hash as a hex string of the file at package_path
        """

        hash_md5 = hashlib.md5()
        with open(package_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def _get_extension_bucket_info(
        self, extension_id: str, package_filename: str
    ) -> Tuple[str, str]:
        """
        Get a bucket url and push id for the extension package

        Parameters
        ----------
        extension_id: str
            name of the extension
        package_filename: str
            Filename to use in bucket for packaged extension

        Returns
        -------
        (str,str)
            (signed_url,bucket_url) for this package
        """
        req = management_pb2.GetExtensionBucketPathRequest(
            parent=self.parent, extension_id=extension_id, file_name=package_filename
        )
        resp = self.client._management.GetExtensionBucketPath(req)
        return resp.signed_url, resp.bucket_path


class Extension(Resource, types.Extension):
    """Extension resource."""

    name_pattern: str = "projects/{project}/extensions/{extension}"
    manager: ExtensionManager
    """ExtensionManager"""

    events: EventManager
    """Event manager."""

    def _init(self):
        self.manager = ExtensionManager(parent=self.parent, client=self.client)
        self.events = EventManager(parent=self.name, client=self.client)
