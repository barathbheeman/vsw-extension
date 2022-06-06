import os
import glob
import subprocess

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

import logging
logger = logging.getLogger(__name__)


class VSCodeWorkspaceOpen(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        homefolder = os.environ['HOME']
        workspace_files = glob.glob(homefolder + '/**/*.code-workspace', recursive=True)
        items = []
        for i in workspace_files:
            data = {'workspace': i}
            items.append(ExtensionResultItem(icon='images/visual-studio-code.png',
                                            name=i.split('/')[-1],
                                            description=i,
                                            on_enter=ExtensionCustomAction(data)))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def open_workspace(self, workspace):
        subprocess.call(f"code {workspace}", shell=True)

    def on_event(self, event, extension):
        data = event.get_data()
        workspace = data['workspace']
        self.open_workspace(workspace)


if __name__ == '__main__':
    VSCodeWorkspaceOpen().run()
