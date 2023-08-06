# coding: utf-8
"""A tornado based Jupyter lab server."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# TODO: import base server app
import os
from jupyter_core.paths import jupyter_config_path, jupyter_path
from notebook.notebookapp import NotebookApp
from traitlets import List, Unicode
from traitlets.config.manager import BaseJSONConfigManager


class LabApp(NotebookApp):

    default_url = Unicode('/lab', config=True,
        help="The default URL to redirect to from `/`"
    )

    extra_labextensions_path = List(Unicode(), config=True,
        help="""extra paths to look for JupyterLab extensions"""
    )

    @property
    def labextensions(self):
        extensions = []
        config_dirs = [os.path.join(p, 'labconfig') for p in
                       jupyter_config_path()]
        for config_dir in config_dirs:
            cm = BaseJSONConfigManager(parent=self, config_dir=config_dir)
            data = cm.get("jupyterlab_config")
            labextensions = (
                data.setdefault("LabApp", {})
                .setdefault("labextensions", {})
            )
            for name, enabled in labextensions.items():
                if enabled:
                    extensions.append(name)
        return extensions

    @property
    def labextensions_path(self):
        """The path to look for JupyterLab extensions"""
        return self.extra_labextensions_path + jupyter_path('labextensions')

    def init_webapp(self):
        super(LabApp, self).init_webapp()
        self.web_app.labextensions = self.labextensions

#-----------------------------------------------------------------------------
# Main entry point
#-----------------------------------------------------------------------------

main = launch_new_instance = LabApp.launch_instance
