from pydantic import Field
from typing import Any
from typing_extensions import TypedDict, NotRequired, Annotated

class Annotations(TypedDict):
    audience: NotRequired[list[str]]
    last_modified: Annotated[NotRequired[str], Field(alias='lastModified')]
    priority: NotRequired[float]

class _Meta(TypedDict):
    pass

class Audiocontent(TypedDict):
    _meta: NotRequired[_Meta]
    annotations: NotRequired[Annotations]
    data: str
    mime_type: Annotated[str, Field(alias='mimeType')]
    type: str

class Basemetadata(TypedDict):
    name: str
    title: NotRequired[str]

class Blobresourcecontents(TypedDict):
    _meta: NotRequired[_Meta]
    blob: str
    mime_type: Annotated[NotRequired[str], Field(alias='mimeType')]
    uri: str

class Booleanschema(TypedDict):
    default: NotRequired[bool]
    description: NotRequired[str]
    title: NotRequired[str]
    type: str

class Arguments(TypedDict):
    pass

class Params(TypedDict):
    arguments: NotRequired[Arguments]
    name: str

class Calltoolrequest(TypedDict):
    method: str
    params: Params

class Structuredcontent(TypedDict):
    pass

class Calltoolresult(TypedDict):
    _meta: NotRequired[_Meta]
    content: list[Any]
    is_error: Annotated[NotRequired[bool], Field(alias='isError')]
    structured_content: Annotated[NotRequired[Structuredcontent], Field(alias='structuredContent')]

class Cancellednotification(TypedDict):
    method: str
    params: Params

class Elicitation(TypedDict):
    pass

class Experimental(TypedDict):
    pass

class Roots(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias='listChanged')]

class Sampling(TypedDict):
    pass

class Clientcapabilities(TypedDict):
    elicitation: NotRequired[Elicitation]
    experimental: NotRequired[Experimental]
    roots: NotRequired[Roots]
    sampling: NotRequired[Sampling]

class Completerequest(TypedDict):
    method: str
    params: Params

class Completion(TypedDict):
    has_more: Annotated[NotRequired[bool], Field(alias='hasMore')]
    total: NotRequired[int]
    values: list[str]

class Completeresult(TypedDict):
    _meta: NotRequired[_Meta]
    completion: Completion

class Createmessagerequest(TypedDict):
    method: str
    params: Params

class Createmessageresult(TypedDict):
    _meta: NotRequired[_Meta]
    content: Any
    model: str
    role: str
    stop_reason: Annotated[NotRequired[str], Field(alias='stopReason')]

class Elicitrequest(TypedDict):
    method: str
    params: Params

class Content(TypedDict):
    pass

class Elicitresult(TypedDict):
    _meta: NotRequired[_Meta]
    action: str
    content: NotRequired[Content]

class Embeddedresource(TypedDict):
    _meta: NotRequired[_Meta]
    annotations: NotRequired[Annotations]
    resource: Any
    type: str

class Result(TypedDict):
    _meta: NotRequired[_Meta]

class Enumschema(TypedDict):
    description: NotRequired[str]
    enum: list[str]
    enum_names: Annotated[NotRequired[list[str]], Field(alias='enumNames')]
    title: NotRequired[str]
    type: str

class Getpromptrequest(TypedDict):
    method: str
    params: Params

class Promptmessage(TypedDict):
    content: Any
    role: str

class Getpromptresult(TypedDict):
    _meta: NotRequired[_Meta]
    description: NotRequired[str]
    messages: list[Promptmessage]

class Imagecontent(TypedDict):
    _meta: NotRequired[_Meta]
    annotations: NotRequired[Annotations]
    data: str
    mime_type: Annotated[str, Field(alias='mimeType')]
    type: str

class Implementation(TypedDict):
    name: str
    title: NotRequired[str]
    version: str

class Initializerequest(TypedDict):
    method: str
    params: Params

class Completions(TypedDict):
    pass

class Logging(TypedDict):
    pass

class Prompts(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias='listChanged')]

class Resources(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias='listChanged')]
    subscribe: NotRequired[bool]

class Tools(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias='listChanged')]

class Servercapabilities(TypedDict):
    completions: NotRequired[Completions]
    experimental: NotRequired[Experimental]
    logging: NotRequired[Logging]
    prompts: NotRequired[Prompts]
    resources: NotRequired[Resources]
    tools: NotRequired[Tools]

class Initializeresult(TypedDict):
    _meta: NotRequired[_Meta]
    capabilities: Servercapabilities
    instructions: NotRequired[str]
    protocol_version: Annotated[str, Field(alias='protocolVersion')]
    server_info: Annotated[Implementation, Field(alias='serverInfo')]

class Initializednotification(TypedDict):
    method: str
    params: NotRequired[Params]

class Error(TypedDict):
    code: int
    data: NotRequired[Any]
    message: str

class Jsonrpcerror(TypedDict):
    error: Error
    id: str | int
    jsonrpc: str

class Jsonrpcnotification(TypedDict):
    jsonrpc: str
    method: str
    params: NotRequired[Params]

class Jsonrpcrequest(TypedDict):
    id: str | int
    jsonrpc: str
    method: str
    params: NotRequired[Params]

class Jsonrpcresponse(TypedDict):
    id: str | int
    jsonrpc: str
    result: Result

class Listpromptsrequest(TypedDict):
    method: str
    params: NotRequired[Params]

class Promptargument(TypedDict):
    description: NotRequired[str]
    name: str
    required: NotRequired[bool]
    title: NotRequired[str]

class Prompt(TypedDict):
    _meta: NotRequired[_Meta]
    arguments: NotRequired[list[Promptargument]]
    description: NotRequired[str]
    name: str
    title: NotRequired[str]

class Listpromptsresult(TypedDict):
    _meta: NotRequired[_Meta]
    next_cursor: Annotated[NotRequired[str], Field(alias='nextCursor')]
    prompts: list[Prompt]

class Listresourcetemplatesrequest(TypedDict):
    method: str
    params: NotRequired[Params]

class Resourcetemplate(TypedDict):
    _meta: NotRequired[_Meta]
    annotations: NotRequired[Annotations]
    description: NotRequired[str]
    mime_type: Annotated[NotRequired[str], Field(alias='mimeType')]
    name: str
    title: NotRequired[str]
    uri_template: Annotated[str, Field(alias='uriTemplate')]

class Listresourcetemplatesresult(TypedDict):
    _meta: NotRequired[_Meta]
    next_cursor: Annotated[NotRequired[str], Field(alias='nextCursor')]
    resource_templates: Annotated[list[Resourcetemplate], Field(alias='resourceTemplates')]

class Listresourcesrequest(TypedDict):
    method: str
    params: NotRequired[Params]

class Resource(TypedDict):
    _meta: NotRequired[_Meta]
    annotations: NotRequired[Annotations]
    description: NotRequired[str]
    mime_type: Annotated[NotRequired[str], Field(alias='mimeType')]
    name: str
    size: NotRequired[int]
    title: NotRequired[str]
    uri: str

class Listresourcesresult(TypedDict):
    _meta: NotRequired[_Meta]
    next_cursor: Annotated[NotRequired[str], Field(alias='nextCursor')]
    resources: list[Resource]

class Listrootsrequest(TypedDict):
    method: str
    params: NotRequired[Params]

class Root(TypedDict):
    _meta: NotRequired[_Meta]
    name: NotRequired[str]
    uri: str

class Listrootsresult(TypedDict):
    _meta: NotRequired[_Meta]
    roots: list[Root]

class Listtoolsrequest(TypedDict):
    method: str
    params: NotRequired[Params]

class Toolannotations(TypedDict):
    destructive_hint: Annotated[NotRequired[bool], Field(alias='destructiveHint')]
    idempotent_hint: Annotated[NotRequired[bool], Field(alias='idempotentHint')]
    open_world_hint: Annotated[NotRequired[bool], Field(alias='openWorldHint')]
    read_only_hint: Annotated[NotRequired[bool], Field(alias='readOnlyHint')]
    title: NotRequired[str]

class Properties(TypedDict):
    pass

class Inputschema(TypedDict):
    properties: NotRequired[Properties]
    required: NotRequired[list[str]]
    type: str

class Outputschema(TypedDict):
    properties: NotRequired[Properties]
    required: NotRequired[list[str]]
    type: str

class Tool(TypedDict):
    _meta: NotRequired[_Meta]
    annotations: NotRequired[Toolannotations]
    description: NotRequired[str]
    input_schema: Annotated[Inputschema, Field(alias='inputSchema')]
    name: str
    output_schema: Annotated[NotRequired[Outputschema], Field(alias='outputSchema')]
    title: NotRequired[str]

class Listtoolsresult(TypedDict):
    _meta: NotRequired[_Meta]
    next_cursor: Annotated[NotRequired[str], Field(alias='nextCursor')]
    tools: list[Tool]

class Loggingmessagenotification(TypedDict):
    method: str
    params: Params

class Modelhint(TypedDict):
    name: NotRequired[str]

class Modelpreferences(TypedDict):
    cost_priority: Annotated[NotRequired[float], Field(alias='costPriority')]
    hints: NotRequired[list[Modelhint]]
    intelligence_priority: Annotated[NotRequired[float], Field(alias='intelligencePriority')]
    speed_priority: Annotated[NotRequired[float], Field(alias='speedPriority')]

class Notification(TypedDict):
    method: str
    params: NotRequired[Params]

class Numberschema(TypedDict):
    description: NotRequired[str]
    maximum: NotRequired[int]
    minimum: NotRequired[int]
    title: NotRequired[str]
    type: str

class Paginatedrequest(TypedDict):
    method: str
    params: NotRequired[Params]

class Paginatedresult(TypedDict):
    _meta: NotRequired[_Meta]
    next_cursor: Annotated[NotRequired[str], Field(alias='nextCursor')]

class Pingrequest(TypedDict):
    method: str
    params: NotRequired[Params]

class Progressnotification(TypedDict):
    method: str
    params: Params

class Promptlistchangednotification(TypedDict):
    method: str
    params: NotRequired[Params]

class Promptreference(TypedDict):
    name: str
    title: NotRequired[str]
    type: str

class Readresourcerequest(TypedDict):
    method: str
    params: Params

class Readresourceresult(TypedDict):
    _meta: NotRequired[_Meta]
    contents: list[Any]

class Request(TypedDict):
    method: str
    params: NotRequired[Params]

class Resourcecontents(TypedDict):
    _meta: NotRequired[_Meta]
    mime_type: Annotated[NotRequired[str], Field(alias='mimeType')]
    uri: str

class Resourcelink(TypedDict):
    _meta: NotRequired[_Meta]
    annotations: NotRequired[Annotations]
    description: NotRequired[str]
    mime_type: Annotated[NotRequired[str], Field(alias='mimeType')]
    name: str
    size: NotRequired[int]
    title: NotRequired[str]
    type: str
    uri: str

class Resourcelistchangednotification(TypedDict):
    method: str
    params: NotRequired[Params]

class Resourcetemplatereference(TypedDict):
    type: str
    uri: str

class Resourceupdatednotification(TypedDict):
    method: str
    params: Params

class Rootslistchangednotification(TypedDict):
    method: str
    params: NotRequired[Params]

class Samplingmessage(TypedDict):
    content: Any
    role: str

class Setlevelrequest(TypedDict):
    method: str
    params: Params

class Stringschema(TypedDict):
    description: NotRequired[str]
    format: NotRequired[str]
    max_length: Annotated[NotRequired[int], Field(alias='maxLength')]
    min_length: Annotated[NotRequired[int], Field(alias='minLength')]
    title: NotRequired[str]
    type: str

class Subscriberequest(TypedDict):
    method: str
    params: Params

class Textcontent(TypedDict):
    _meta: NotRequired[_Meta]
    annotations: NotRequired[Annotations]
    text: str
    type: str

class Textresourcecontents(TypedDict):
    _meta: NotRequired[_Meta]
    mime_type: Annotated[NotRequired[str], Field(alias='mimeType')]
    text: str
    uri: str

class Toollistchangednotification(TypedDict):
    method: str
    params: NotRequired[Params]

class Unsubscriberequest(TypedDict):
    method: str
    params: Params