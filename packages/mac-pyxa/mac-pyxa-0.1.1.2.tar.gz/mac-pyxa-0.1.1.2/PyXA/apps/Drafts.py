""".. versionadded:: 0.0.8

Control Drafts using JXA-like syntax.
"""

from datetime import datetime
from typing import Union

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath

class XADraftsApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with Drafts.app.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the application.
        """
        return self.xa_scel.name()

    @property
    def version(self) -> str:
        """The version of Drafts.app.
        """
        return self.xa_scel.version()

    def new_draft(self, content: str) -> 'XADraftsDraft':
        """Creates a new draft with the given name and content

        :param content: The full content of the draft (the first line is the name)
        :type content: str
        :return: The newly created draft object
        :rtype: XADraftsDraft

        .. versionadded:: 0.0.8
        """
        new_draft = self.make("draft", {"content": content})
        self.drafts().push(new_draft)
        print(self.drafts().content())
        return self.drafts().last()

    def drafts(self, filter: Union[dict, None] = None) -> 'XADraftsDraftList':
        """Returns a list of drafts, as PyXA-wrapped objects, matching the given filter.

        :param filter: Keys and values to filter drafts by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of drafts
        :rtype: XADraftsDraftList

        .. versionadded:: 0.0.8
        """
        return self._new_element(self.xa_scel.drafts(), XADraftsDraftList, filter)

    def make(self, specifier: str, properties: dict = None):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: str
        :param properties: The properties to give the object
        :type properties: dict
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        .. versionadded:: 0.0.8
        """
        if properties is None:
            properties = {}

        obj = self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)

        if specifier == "draft":
            return self._new_element(obj, XADraftsDraft)




class XADraftsDraftList(XABase.XAList):
    """A wrapper around a list of drafts.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XADraftsDraft, filter)

    def id(self) -> list[str]:
        """Gets the ID of each draft in the list.

        :return: A list of draft IDs
        :rtype: list[str]
        
        .. versionadded:: 0.0.8
        """
        return list(self.xa_elem.arrayByApplyingSelector_("id"))

    def name(self) -> list[str]:
        """Gets the name of each draft in the list.

        :return: A list of draft names
        :rtype: list[str]
        
        .. versionadded:: 0.0.8
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def content(self) -> list[str]:
        """Gets the content of each draft in the list.

        :return: A list of draft contents
        :rtype: list[str]
        
        .. versionadded:: 0.0.8
        """
        return list(self.xa_elem.arrayByApplyingSelector_("content"))

    def flagged(self) -> list[bool]:
        """Gets the flagged status of each draft in the list.

        :return: A list of draft flagged statuses
        :rtype: list[bool]
        
        .. versionadded:: 0.0.8
        """
        return list(self.xa_elem.arrayByApplyingSelector_("flagged"))

    def tags(self) -> list[list[str]]:
        """Gets the tags of each draft in the list.

        :return: A list of draft tags
        :rtype: list[list[str]]
        
        .. versionadded:: 0.0.8
        """
        return list(self.xa_elem.arrayByApplyingSelector_("tags"))

    def created_at(self) -> list[datetime]:
        """Gets the creation date of each draft in the list.

        :return: A list of draft creation dates
        :rtype: list[datetime]
        
        .. versionadded:: 0.0.8
        """
        return list(self.xa_elem.arrayByApplyingSelector_("createdAt"))

    def modified_at(self) -> list[datetime]:
        """Gets the last modification date of each draft in the list.

        :return: A list of draft modification dates
        :rtype: list[datetime]
        
        .. versionadded:: 0.0.8
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modifiedAt"))

    def accessed_at(self) -> list[datetime]:
        """Gets the last access date of each draft in the list.

        :return: A list of draft last access dates
        :rtype: list[datetime]
        
        .. versionadded:: 0.0.8
        """
        return list(self.xa_elem.arrayByApplyingSelector_("accessedAt"))

    def permalink(self) -> list[str]:
        """Gets the URL of each draft in the list.

        :return: A list of draft URLs
        :rtype: list[str]
        
        .. versionadded:: 0.0.8
        """
        return list(self.xa_elem.arrayByApplyingSelector_("permalink"))

    def by_id(self, id: str) -> Union['XADraftsDraft', None]:
        """Retrieves the draft whose ID matches the given ID, if one exists.

        :return: The desired draft, if it is found
        :rtype: Union[XADraftsDraft, None]
        
        .. versionadded:: 0.0.8
        """
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union['XADraftsDraft', None]:
        """Retrieves the draft whose name matches the given name, if one exists.

        :return: The desired draft, if it is found
        :rtype: Union[XADraftsDraft, None]
        
        .. versionadded:: 0.0.8
        """
        return self.by_property("name", name)

    def by_content(self, content: str) -> Union['XADraftsDraft', None]:
        """Retrieves the draft whose content matches the given content, if one exists.

        :return: The desired draft, if it is found
        :rtype: Union[XADraftsDraft, None]
        
        .. versionadded:: 0.0.8
        """
        return self.by_property("content", content)

    def by_flagged(self, flagged: bool) -> Union['XADraftsDraft', None]:
        """Retrieves the first draft whose flagged status matches the given boolean value, if one exists.

        :return: The desired draft, if it is found
        :rtype: Union[XADraftsDraft, None]
        
        .. versionadded:: 0.0.8
        """
        return self.by_property("flagged", flagged)

    def by_tags(self, tags: list[str]) -> Union['XADraftsDraft', None]:
        """Retrieves the first draft whose list of tags matches the given list, if one exists.

        :return: The desired draft, if it is found
        :rtype: Union[XADraftsDraft, None]
        
        .. versionadded:: 0.0.8
        """
        return self.by_property("tags", tags)

    def by_created_at(self, created_at: datetime) -> Union['XADraftsDraft', None]:
        """Retrieves the draft whose creation date matches the given date, if one exists.

        :return: The desired draft, if it is found
        :rtype: Union[XADraftsDraft, None]
        
        .. versionadded:: 0.0.8
        """
        return self.by_property("createdAt", created_at)

    def by_modified_at(self, modified_at: datetime) -> Union['XADraftsDraft', None]:
        """Retrieves the draft whose last modification date matches the given date, if one exists.

        :return: The desired draft, if it is found
        :rtype: Union[XADraftsDraft, None]
        
        .. versionadded:: 0.0.8
        """
        return self.by_property("modifiedAt", modified_at)

    def by_accessed_at(self, accessed_at: datetime) -> Union['XADraftsDraft', None]:
        """Retrieves the draft whose last access date matches the given date, if one exists.

        :return: The desired draft, if it is found
        :rtype: Union[XADraftsDraft, None]
        
        .. versionadded:: 0.0.8
        """
        return self.by_property("accessedAt", accessed_at)

    def by_permalink(self, permalink: str) -> Union['XADraftsDraft', None]:
        """Retrieves the draft whose URL matches the given URL, if one exists.

        :return: The desired draft, if it is found
        :rtype: Union[XADraftsDraft, None]
        
        .. versionadded:: 0.0.8
        """
        return self.by_property("permalink", permalink)

class XADraftsDraft(XABase.XAObject):
    """A draft in Drafts.app.

    .. versionadded:: 0.0.8
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> str:
        """The unique identifier of the draft.
        """
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The first line of the draft.
        """
        return self.xa_elem.name()

    @property
    def content(self) -> str:
        """The content of the draft.
        """
        return self.xa_elem.content()

    @content.setter
    def content(self, content: str):
        self.set_property("content", content)

    @property
    def flagged(self) -> bool:
        """The flagged status of the draft.
        """
        return self.xa_elem.flagged()

    @flagged.setter
    def flagged(self, flagged: bool):
        self.set_property("flagged", flagged)

    @property
    def tags(self) -> list[str]:
        """The tags assigned to the draft.
        """
        return self.xa_elem.tags()
    
    @tags.setter
    def tags(self, tags: list[str]):
        self.set_property("tags", tags)

    @property
    def created_at(self) -> datetime:
        """The date the draft was created.
        """
        return self.xa_elem.createdAt()

    @property
    def modified_at(self) -> datetime:
        """The date the draft was last modified.
        """
        return self.xa_elem.modifiedAt()

    @property
    def accessed_at(self) -> datetime:
        """The date the draft was last accessed.
        """
        return self.xa_elem.accessedAt()

    @property
    def permalink(self) -> str:
        """The URL of the draft.
        """
        return self.xa_elem.permalink()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"