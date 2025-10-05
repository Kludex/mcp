from typing import Annotated, Any, Literal

from pydantic import Field, with_config
from typing_extensions import NotRequired, TypedDict


class Annotations(TypedDict):
    audience: NotRequired[list[str]]
    last_modified: Annotated[NotRequired[str], Field(alias="lastModified")]
    priority: NotRequired[float]


@with_config(extra="allow")
class Meta(TypedDict):
    pass


class AudioContent(TypedDict):
    _meta: NotRequired[Meta]
    annotations: NotRequired[Annotations]
    data: str
    mime_type: Annotated[str, Field(alias="mimeType")]
    type: Literal["audio"]


class BaseMetadata(TypedDict):
    name: str
    title: NotRequired[str]


@with_config(extra="allow")
class BlobResourceContentsMeta(TypedDict):
    pass


class BlobResourceContents(TypedDict):
    _meta: NotRequired[BlobResourceContentsMeta]
    blob: str
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    uri: str


class BooleanSchema(TypedDict):
    default: NotRequired[bool]
    description: NotRequired[str]
    title: NotRequired[str]
    type: Literal["boolean"]


@with_config(extra="allow")
class Arguments(TypedDict):
    pass


class Params(TypedDict):
    arguments: NotRequired[Arguments]
    name: str


class CallToolRequest(TypedDict):
    method: Literal["tools/call"]
    params: Params


@with_config(extra="allow")
class CallToolResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class ContentBlockMeta(TypedDict):
    pass


class TextContent(TypedDict):
    _meta: NotRequired[ContentBlockMeta]
    annotations: NotRequired[Annotations]
    text: str
    type: Literal["text"]


class ImageContent(TypedDict):
    _meta: NotRequired[ContentBlockMeta]
    annotations: NotRequired[Annotations]
    data: str
    mime_type: Annotated[str, Field(alias="mimeType")]
    type: Literal["image"]


class ResourceLink(TypedDict):
    _meta: NotRequired[ContentBlockMeta]
    annotations: NotRequired[Annotations]
    description: NotRequired[str]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    name: str
    size: NotRequired[int]
    title: NotRequired[str]
    type: Literal["resource_link"]
    uri: str


@with_config(extra="allow")
class ResourceMeta(TypedDict):
    pass


class TextResourceContents(TypedDict):
    _meta: NotRequired[ResourceMeta]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    text: str
    uri: str


class EmbeddedResource(TypedDict):
    _meta: NotRequired[ContentBlockMeta]
    annotations: NotRequired[Annotations]
    resource: TextResourceContents | BlobResourceContents
    type: Literal["resource"]


@with_config(extra="allow")
class StructuredContent(TypedDict):
    pass


class CallToolResult(TypedDict):
    _meta: NotRequired[CallToolResultMeta]
    content: list[TextContent | ImageContent | AudioContent | ResourceLink | EmbeddedResource]
    is_error: Annotated[NotRequired[bool], Field(alias="isError")]
    structured_content: Annotated[NotRequired[StructuredContent], Field(alias="structuredContent")]


class CancelledNotificationParams(TypedDict):
    reason: NotRequired[str]
    request_id: Annotated[str | int, Field(alias="requestId")]


class CancelledNotification(TypedDict):
    method: Literal["notifications/cancelled"]
    params: CancelledNotificationParams


@with_config(extra="allow")
class Elicitation(TypedDict):
    pass


@with_config(extra="allow")
class Experimental(TypedDict):
    pass


class Roots(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias="listChanged")]


@with_config(extra="allow")
class Sampling(TypedDict):
    pass


class ClientCapabilities(TypedDict):
    elicitation: NotRequired[Elicitation]
    experimental: NotRequired[Experimental]
    roots: NotRequired[Roots]
    sampling: NotRequired[Sampling]


@with_config(extra="allow")
class ParamsMeta(TypedDict):
    pass


@with_config(extra="allow")
class ClientNotificationParams(TypedDict):
    _meta: NotRequired[ParamsMeta]


class InitializedNotification(TypedDict):
    method: Literal["notifications/initialized"]
    params: NotRequired[ClientNotificationParams]


class ProgressNotification(TypedDict):
    method: Literal["notifications/progress"]
    params: ClientNotificationParams


class RootsListChangedNotification(TypedDict):
    method: Literal["notifications/roots/list_changed"]
    params: NotRequired[ClientNotificationParams]


class Implementation(TypedDict):
    name: str
    title: NotRequired[str]
    version: str


class ClientRequestParams(TypedDict):
    capabilities: ClientCapabilities
    client_info: Annotated[Implementation, Field(alias="clientInfo")]
    protocol_version: Annotated[str, Field(alias="protocolVersion")]


class InitializeRequest(TypedDict):
    method: Literal["initialize"]
    params: ClientRequestParams


class PingRequest(TypedDict):
    method: Literal["ping"]
    params: NotRequired[ClientRequestParams]


class ListResourcesRequest(TypedDict):
    method: Literal["resources/list"]
    params: NotRequired[ClientRequestParams]


class ListResourceTemplatesRequest(TypedDict):
    method: Literal["resources/templates/list"]
    params: NotRequired[ClientRequestParams]


class ReadResourceRequest(TypedDict):
    method: Literal["resources/read"]
    params: ClientRequestParams


class SubscribeRequest(TypedDict):
    method: Literal["resources/subscribe"]
    params: ClientRequestParams


class UnsubscribeRequest(TypedDict):
    method: Literal["resources/unsubscribe"]
    params: ClientRequestParams


class ListPromptsRequest(TypedDict):
    method: Literal["prompts/list"]
    params: NotRequired[ClientRequestParams]


class GetPromptRequest(TypedDict):
    method: Literal["prompts/get"]
    params: ClientRequestParams


class ListToolsRequest(TypedDict):
    method: Literal["tools/list"]
    params: NotRequired[ClientRequestParams]


class SetLevelRequest(TypedDict):
    method: Literal["logging/setLevel"]
    params: ClientRequestParams


class CompleteRequest(TypedDict):
    method: Literal["completion/complete"]
    params: ClientRequestParams


@with_config(extra="allow")
class ClientResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class Result(TypedDict):
    _meta: NotRequired[ClientResultMeta]


class CreateMessageResult(TypedDict):
    _meta: NotRequired[ClientResultMeta]
    content: TextContent | ImageContent | AudioContent
    model: str
    role: str
    stop_reason: Annotated[NotRequired[str], Field(alias="stopReason")]


@with_config(extra="allow")
class RootsMeta(TypedDict):
    pass


class Root(TypedDict):
    _meta: NotRequired[RootsMeta]
    name: NotRequired[str]
    uri: str


class ListRootsResult(TypedDict):
    _meta: NotRequired[ClientResultMeta]
    roots: list[Root]


@with_config(extra="allow")
class Content(TypedDict):
    pass


class ElicitResult(TypedDict):
    _meta: NotRequired[ClientResultMeta]
    action: str
    content: NotRequired[Content]


class Argument(TypedDict):
    name: str
    value: str


@with_config(extra="allow")
class ContextArguments(TypedDict):
    pass


class Context(TypedDict):
    arguments: NotRequired[ContextArguments]


class PromptReference(TypedDict):
    name: str
    title: NotRequired[str]
    type: Literal["ref/prompt"]


class ResourceTemplateReference(TypedDict):
    type: Literal["ref/resource"]
    uri: str


class CompleteRequestParams(TypedDict):
    argument: Argument
    context: NotRequired[Context]
    ref: PromptReference | ResourceTemplateReference


class ClientResultCompleteRequest(TypedDict):
    method: Literal["completion/complete"]
    params: CompleteRequestParams


@with_config(extra="allow")
class CompleteResultMeta(TypedDict):
    pass


class Completion(TypedDict):
    has_more: Annotated[NotRequired[bool], Field(alias="hasMore")]
    total: NotRequired[int]
    values: list[str]


class CompleteResult(TypedDict):
    _meta: NotRequired[CompleteResultMeta]
    completion: Completion


class SamplingMessage(TypedDict):
    content: TextContent | ImageContent | AudioContent
    role: str


@with_config(extra="allow")
class Metadata(TypedDict):
    pass


class ModelHint(TypedDict):
    name: NotRequired[str]


class ModelPreferences(TypedDict):
    cost_priority: Annotated[NotRequired[float], Field(alias="costPriority")]
    hints: NotRequired[list[ModelHint]]
    intelligence_priority: Annotated[NotRequired[float], Field(alias="intelligencePriority")]
    speed_priority: Annotated[NotRequired[float], Field(alias="speedPriority")]


class CreateMessageRequestParams(TypedDict):
    include_context: Annotated[NotRequired[str], Field(alias="includeContext")]
    max_tokens: Annotated[int, Field(alias="maxTokens")]
    messages: list[SamplingMessage]
    metadata: NotRequired[Metadata]
    model_preferences: Annotated[NotRequired[ModelPreferences], Field(alias="modelPreferences")]
    stop_sequences: Annotated[NotRequired[list[str]], Field(alias="stopSequences")]
    system_prompt: Annotated[NotRequired[str], Field(alias="systemPrompt")]
    temperature: NotRequired[float]


class CreateMessageRequest(TypedDict):
    method: Literal["sampling/createMessage"]
    params: CreateMessageRequestParams


@with_config(extra="allow")
class CreateMessageResultMeta(TypedDict):
    pass


class ModelPreferencesCreateMessageResult(TypedDict):
    _meta: NotRequired[CreateMessageResultMeta]
    content: TextContent | ImageContent | AudioContent
    model: str
    role: str
    stop_reason: Annotated[NotRequired[str], Field(alias="stopReason")]


@with_config(extra="allow")
class Properties(TypedDict):
    pass


class RequestedSchema(TypedDict):
    properties: Properties
    required: NotRequired[list[str]]
    type: Literal["object"]


class ElicitRequestParams(TypedDict):
    message: str
    requested_schema: Annotated[RequestedSchema, Field(alias="requestedSchema")]


class ElicitRequest(TypedDict):
    method: Literal["elicitation/create"]
    params: ElicitRequestParams


@with_config(extra="allow")
class ElicitResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class ElicitResultContent(TypedDict):
    pass


class RoleElicitResult(TypedDict):
    _meta: NotRequired[ElicitResultMeta]
    action: str
    content: NotRequired[ElicitResultContent]


@with_config(extra="allow")
class EmbeddedResourceMeta(TypedDict):
    pass


class RoleEmbeddedResource(TypedDict):
    _meta: NotRequired[EmbeddedResourceMeta]
    annotations: NotRequired[Annotations]
    resource: TextResourceContents | BlobResourceContents
    type: Literal["resource"]


class EnumSchema(TypedDict):
    description: NotRequired[str]
    enum: list[str]
    enum_names: Annotated[NotRequired[list[str]], Field(alias="enumNames")]
    title: NotRequired[str]
    type: Literal["string"]


@with_config(extra="allow")
class ParamsArguments(TypedDict):
    pass


class GetPromptRequestParams(TypedDict):
    arguments: NotRequired[ParamsArguments]
    name: str


class EmptyResultGetPromptRequest(TypedDict):
    method: Literal["prompts/get"]
    params: GetPromptRequestParams


@with_config(extra="allow")
class GetPromptResultMeta(TypedDict):
    pass


class PromptMessage(TypedDict):
    content: TextContent | ImageContent | AudioContent | ResourceLink | EmbeddedResource
    role: str


class GetPromptResult(TypedDict):
    _meta: NotRequired[GetPromptResultMeta]
    description: NotRequired[str]
    messages: list[PromptMessage]


@with_config(extra="allow")
class ImageContentMeta(TypedDict):
    pass


class RoleImageContent(TypedDict):
    _meta: NotRequired[ImageContentMeta]
    annotations: NotRequired[Annotations]
    data: str
    mime_type: Annotated[str, Field(alias="mimeType")]
    type: Literal["image"]


class AnnotationsImplementation(TypedDict):
    name: str
    title: NotRequired[str]
    version: str


class InitializeRequestParams(TypedDict):
    capabilities: ClientCapabilities
    client_info: Annotated[Implementation, Field(alias="clientInfo")]
    protocol_version: Annotated[str, Field(alias="protocolVersion")]


class AnnotationsInitializeRequest(TypedDict):
    method: Literal["initialize"]
    params: InitializeRequestParams


@with_config(extra="allow")
class InitializeResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class Completions(TypedDict):
    pass


@with_config(extra="allow")
class CapabilitiesExperimental(TypedDict):
    pass


@with_config(extra="allow")
class Logging(TypedDict):
    pass


class Prompts(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias="listChanged")]


class Resources(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias="listChanged")]
    subscribe: NotRequired[bool]


class Tools(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias="listChanged")]


class ServerCapabilities(TypedDict):
    completions: NotRequired[Completions]
    experimental: NotRequired[CapabilitiesExperimental]
    logging: NotRequired[Logging]
    prompts: NotRequired[Prompts]
    resources: NotRequired[Resources]
    tools: NotRequired[Tools]


class InitializeResult(TypedDict):
    _meta: NotRequired[InitializeResultMeta]
    capabilities: ServerCapabilities
    instructions: NotRequired[str]
    protocol_version: Annotated[str, Field(alias="protocolVersion")]
    server_info: Annotated[Implementation, Field(alias="serverInfo")]


@with_config(extra="allow")
class InitializedNotificationParams(TypedDict):
    _meta: NotRequired[ParamsMeta]


class ServerInfoInitializedNotification(TypedDict):
    method: Literal["notifications/initialized"]
    params: NotRequired[InitializedNotificationParams]


class Error(TypedDict):
    code: int
    data: NotRequired[Any]
    message: str


class JSONRPCError(TypedDict):
    error: Error
    id: str | int
    jsonrpc: Literal["2.0"]


@with_config(extra="allow")
class IdParams(TypedDict):
    _meta: NotRequired[ParamsMeta]


class JSONRPCRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: str
    params: NotRequired[IdParams]


@with_config(extra="allow")
class JSONRPCMessageParams(TypedDict):
    _meta: NotRequired[ParamsMeta]


class JSONRPCNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: str
    params: NotRequired[JSONRPCMessageParams]


class JSONRPCResponse(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    result: Result


@with_config(extra="allow")
class JSONRPCNotificationParams(TypedDict):
    _meta: NotRequired[ParamsMeta]


class JSONRPCMessageJSONRPCNotification(TypedDict):
    jsonrpc: Literal["2.0"]
    method: str
    params: NotRequired[JSONRPCNotificationParams]


class JSONRPCMessageJSONRPCRequest(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    method: str
    params: NotRequired[IdParams]


class IdJSONRPCResponse(TypedDict):
    id: str | int
    jsonrpc: Literal["2.0"]
    result: Result


class ListPromptsRequestParams(TypedDict):
    cursor: NotRequired[str]


class ResultListPromptsRequest(TypedDict):
    method: Literal["prompts/list"]
    params: NotRequired[ListPromptsRequestParams]


@with_config(extra="allow")
class ListPromptsResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class PromptsMeta(TypedDict):
    pass


class PromptArgument(TypedDict):
    description: NotRequired[str]
    name: str
    required: NotRequired[bool]
    title: NotRequired[str]


class Prompt(TypedDict):
    _meta: NotRequired[PromptsMeta]
    arguments: NotRequired[list[PromptArgument]]
    description: NotRequired[str]
    name: str
    title: NotRequired[str]


class ListPromptsResult(TypedDict):
    _meta: NotRequired[ListPromptsResultMeta]
    next_cursor: Annotated[NotRequired[str], Field(alias="nextCursor")]
    prompts: list[Prompt]


class ListResourceTemplatesRequestParams(TypedDict):
    cursor: NotRequired[str]


class ResultListResourceTemplatesRequest(TypedDict):
    method: Literal["resources/templates/list"]
    params: NotRequired[ListResourceTemplatesRequestParams]


@with_config(extra="allow")
class ListResourceTemplatesResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class ResourceTemplatesMeta(TypedDict):
    pass


class ResourceTemplate(TypedDict):
    _meta: NotRequired[ResourceTemplatesMeta]
    annotations: NotRequired[Annotations]
    description: NotRequired[str]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    name: str
    title: NotRequired[str]
    uri_template: Annotated[str, Field(alias="uriTemplate")]


class ListResourceTemplatesResult(TypedDict):
    _meta: NotRequired[ListResourceTemplatesResultMeta]
    next_cursor: Annotated[NotRequired[str], Field(alias="nextCursor")]
    resource_templates: Annotated[list[ResourceTemplate], Field(alias="resourceTemplates")]


class ListResourcesRequestParams(TypedDict):
    cursor: NotRequired[str]


class AnnotationsListResourcesRequest(TypedDict):
    method: Literal["resources/list"]
    params: NotRequired[ListResourcesRequestParams]


@with_config(extra="allow")
class ListResourcesResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class ResourcesMeta(TypedDict):
    pass


class Resource(TypedDict):
    _meta: NotRequired[ResourcesMeta]
    annotations: NotRequired[Annotations]
    description: NotRequired[str]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    name: str
    size: NotRequired[int]
    title: NotRequired[str]
    uri: str


class ListResourcesResult(TypedDict):
    _meta: NotRequired[ListResourcesResultMeta]
    next_cursor: Annotated[NotRequired[str], Field(alias="nextCursor")]
    resources: list[Resource]


@with_config(extra="allow")
class ListRootsRequestParams(TypedDict):
    _meta: NotRequired[ParamsMeta]


class ListRootsRequest(TypedDict):
    method: Literal["roots/list"]
    params: NotRequired[ListRootsRequestParams]


@with_config(extra="allow")
class ListRootsResultMeta(TypedDict):
    pass


class AnnotationsListRootsResult(TypedDict):
    _meta: NotRequired[ListRootsResultMeta]
    roots: list[Root]


class ListToolsRequestParams(TypedDict):
    cursor: NotRequired[str]


class AnnotationsListToolsRequest(TypedDict):
    method: Literal["tools/list"]
    params: NotRequired[ListToolsRequestParams]


@with_config(extra="allow")
class ListToolsResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class ToolsMeta(TypedDict):
    pass


class ToolAnnotations(TypedDict):
    destructive_hint: Annotated[NotRequired[bool], Field(alias="destructiveHint")]
    idempotent_hint: Annotated[NotRequired[bool], Field(alias="idempotentHint")]
    open_world_hint: Annotated[NotRequired[bool], Field(alias="openWorldHint")]
    read_only_hint: Annotated[NotRequired[bool], Field(alias="readOnlyHint")]
    title: NotRequired[str]


@with_config(extra="allow")
class InputSchemaProperties(TypedDict):
    pass


class InputSchema(TypedDict):
    properties: NotRequired[InputSchemaProperties]
    required: NotRequired[list[str]]
    type: Literal["object"]


@with_config(extra="allow")
class OutputSchemaProperties(TypedDict):
    pass


class OutputSchema(TypedDict):
    properties: NotRequired[OutputSchemaProperties]
    required: NotRequired[list[str]]
    type: Literal["object"]


class Tool(TypedDict):
    _meta: NotRequired[ToolsMeta]
    annotations: NotRequired[ToolAnnotations]
    description: NotRequired[str]
    input_schema: Annotated[InputSchema, Field(alias="inputSchema")]
    name: str
    output_schema: Annotated[NotRequired[OutputSchema], Field(alias="outputSchema")]
    title: NotRequired[str]


class ListToolsResult(TypedDict):
    _meta: NotRequired[ListToolsResultMeta]
    next_cursor: Annotated[NotRequired[str], Field(alias="nextCursor")]
    tools: list[Tool]


class LoggingMessageNotificationParams(TypedDict):
    data: Any
    level: str
    logger: NotRequired[str]


class LoggingMessageNotification(TypedDict):
    method: Literal["notifications/message"]
    params: LoggingMessageNotificationParams


class LevelModelHint(TypedDict):
    name: NotRequired[str]


class LevelModelPreferences(TypedDict):
    cost_priority: Annotated[NotRequired[float], Field(alias="costPriority")]
    hints: NotRequired[list[ModelHint]]
    intelligence_priority: Annotated[NotRequired[float], Field(alias="intelligencePriority")]
    speed_priority: Annotated[NotRequired[float], Field(alias="speedPriority")]


@with_config(extra="allow")
class NotificationParams(TypedDict):
    _meta: NotRequired[ParamsMeta]


class Notification(TypedDict):
    method: str
    params: NotRequired[NotificationParams]


class NumberSchema(TypedDict):
    description: NotRequired[str]
    maximum: NotRequired[int]
    minimum: NotRequired[int]
    title: NotRequired[str]
    type: str


class PaginatedRequestParams(TypedDict):
    cursor: NotRequired[str]


class PaginatedRequest(TypedDict):
    method: str
    params: NotRequired[PaginatedRequestParams]


@with_config(extra="allow")
class PaginatedResultMeta(TypedDict):
    pass


class PaginatedResult(TypedDict):
    _meta: NotRequired[PaginatedResultMeta]
    next_cursor: Annotated[NotRequired[str], Field(alias="nextCursor")]


@with_config(extra="allow")
class PingRequestParams(TypedDict):
    _meta: NotRequired[ParamsMeta]


class LevelPingRequest(TypedDict):
    method: Literal["ping"]
    params: NotRequired[PingRequestParams]


class StringSchema(TypedDict):
    description: NotRequired[str]
    format: NotRequired[str]
    max_length: Annotated[NotRequired[int], Field(alias="maxLength")]
    min_length: Annotated[NotRequired[int], Field(alias="minLength")]
    title: NotRequired[str]
    type: Literal["string"]


class ProgressNotificationParams(TypedDict):
    message: NotRequired[str]
    progress: float
    progress_token: Annotated[str | int, Field(alias="progressToken")]
    total: NotRequired[float]


class PrimitiveSchemaDefinitionProgressNotification(TypedDict):
    method: Literal["notifications/progress"]
    params: ProgressNotificationParams


@with_config(extra="allow")
class PromptMeta(TypedDict):
    pass


class ProgressTokenPrompt(TypedDict):
    _meta: NotRequired[PromptMeta]
    arguments: NotRequired[list[PromptArgument]]
    description: NotRequired[str]
    name: str
    title: NotRequired[str]


class ProgressTokenPromptArgument(TypedDict):
    description: NotRequired[str]
    name: str
    required: NotRequired[bool]
    title: NotRequired[str]


@with_config(extra="allow")
class PromptListChangedNotificationParams(TypedDict):
    _meta: NotRequired[ParamsMeta]


class PromptListChangedNotification(TypedDict):
    method: Literal["notifications/prompts/list_changed"]
    params: NotRequired[PromptListChangedNotificationParams]


class ProgressTokenPromptMessage(TypedDict):
    content: TextContent | ImageContent | AudioContent | ResourceLink | EmbeddedResource
    role: str


class RolePromptReference(TypedDict):
    name: str
    title: NotRequired[str]
    type: Literal["ref/prompt"]


class ReadResourceRequestParams(TypedDict):
    uri: str


class RoleReadResourceRequest(TypedDict):
    method: Literal["resources/read"]
    params: ReadResourceRequestParams


@with_config(extra="allow")
class ReadResourceResultMeta(TypedDict):
    pass


class ReadResourceResult(TypedDict):
    _meta: NotRequired[ReadResourceResultMeta]
    contents: list[TextResourceContents | BlobResourceContents]


@with_config(extra="allow")
class RequestParams(TypedDict):
    _meta: NotRequired[ParamsMeta]


class Request(TypedDict):
    method: str
    params: NotRequired[RequestParams]


class RoleResource(TypedDict):
    _meta: NotRequired[ResourceMeta]
    annotations: NotRequired[Annotations]
    description: NotRequired[str]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    name: str
    size: NotRequired[int]
    title: NotRequired[str]
    uri: str


@with_config(extra="allow")
class ResourceContentsMeta(TypedDict):
    pass


class ResourceContents(TypedDict):
    _meta: NotRequired[ResourceContentsMeta]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    uri: str


@with_config(extra="allow")
class ResourceLinkMeta(TypedDict):
    pass


class AnnotationsResourceLink(TypedDict):
    _meta: NotRequired[ResourceLinkMeta]
    annotations: NotRequired[Annotations]
    description: NotRequired[str]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    name: str
    size: NotRequired[int]
    title: NotRequired[str]
    type: Literal["resource_link"]
    uri: str


@with_config(extra="allow")
class ResourceListChangedNotificationParams(TypedDict):
    _meta: NotRequired[ParamsMeta]


class ResourceListChangedNotification(TypedDict):
    method: Literal["notifications/resources/list_changed"]
    params: NotRequired[ResourceListChangedNotificationParams]


@with_config(extra="allow")
class ResourceTemplateMeta(TypedDict):
    pass


class AnnotationsResourceTemplate(TypedDict):
    _meta: NotRequired[ResourceTemplateMeta]
    annotations: NotRequired[Annotations]
    description: NotRequired[str]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    name: str
    title: NotRequired[str]
    uri_template: Annotated[str, Field(alias="uriTemplate")]


class AnnotationsResourceTemplateReference(TypedDict):
    type: Literal["ref/resource"]
    uri: str


class ResourceUpdatedNotificationParams(TypedDict):
    uri: str


class ResourceUpdatedNotification(TypedDict):
    method: Literal["notifications/resources/updated"]
    params: ResourceUpdatedNotificationParams


@with_config(extra="allow")
class ResultMeta(TypedDict):
    pass


@with_config(extra="allow")
class AnnotationsResult(TypedDict):
    _meta: NotRequired[ResultMeta]


@with_config(extra="allow")
class RootMeta(TypedDict):
    pass


class AnnotationsRoot(TypedDict):
    _meta: NotRequired[RootMeta]
    name: NotRequired[str]
    uri: str


@with_config(extra="allow")
class RootsListChangedNotificationParams(TypedDict):
    _meta: NotRequired[ParamsMeta]


class AnnotationsRootsListChangedNotification(TypedDict):
    method: Literal["notifications/roots/list_changed"]
    params: NotRequired[RootsListChangedNotificationParams]


class AnnotationsSamplingMessage(TypedDict):
    content: TextContent | ImageContent | AudioContent
    role: str


@with_config(extra="allow")
class ServerCapabilitiesCompletions(TypedDict):
    pass


@with_config(extra="allow")
class ServerCapabilitiesExperimental(TypedDict):
    pass


@with_config(extra="allow")
class ServerCapabilitiesLogging(TypedDict):
    pass


class ServerCapabilitiesPrompts(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias="listChanged")]


class ServerCapabilitiesResources(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias="listChanged")]
    subscribe: NotRequired[bool]


class ServerCapabilitiesTools(TypedDict):
    list_changed: Annotated[NotRequired[bool], Field(alias="listChanged")]


class RoleServerCapabilities(TypedDict):
    completions: NotRequired[ServerCapabilitiesCompletions]
    experimental: NotRequired[ServerCapabilitiesExperimental]
    logging: NotRequired[ServerCapabilitiesLogging]
    prompts: NotRequired[ServerCapabilitiesPrompts]
    resources: NotRequired[ServerCapabilitiesResources]
    tools: NotRequired[ServerCapabilitiesTools]


@with_config(extra="allow")
class ServerNotificationParams(TypedDict):
    _meta: NotRequired[ParamsMeta]


class ToolListChangedNotification(TypedDict):
    method: Literal["notifications/tools/list_changed"]
    params: NotRequired[ServerNotificationParams]


class SetLevelRequestParams(TypedDict):
    level: str


class ServerResultSetLevelRequest(TypedDict):
    method: Literal["logging/setLevel"]
    params: SetLevelRequestParams


class LevelStringSchema(TypedDict):
    description: NotRequired[str]
    format: NotRequired[str]
    max_length: Annotated[NotRequired[int], Field(alias="maxLength")]
    min_length: Annotated[NotRequired[int], Field(alias="minLength")]
    title: NotRequired[str]
    type: Literal["string"]


class SubscribeRequestParams(TypedDict):
    uri: str


class LevelSubscribeRequest(TypedDict):
    method: Literal["resources/subscribe"]
    params: SubscribeRequestParams


@with_config(extra="allow")
class TextContentMeta(TypedDict):
    pass


class LevelTextContent(TypedDict):
    _meta: NotRequired[TextContentMeta]
    annotations: NotRequired[Annotations]
    text: str
    type: Literal["text"]


@with_config(extra="allow")
class TextResourceContentsMeta(TypedDict):
    pass


class AnnotationsTextResourceContents(TypedDict):
    _meta: NotRequired[TextResourceContentsMeta]
    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    text: str
    uri: str


@with_config(extra="allow")
class ToolMeta(TypedDict):
    pass


class AnnotationsInputSchema(TypedDict):
    properties: NotRequired[InputSchemaProperties]
    required: NotRequired[list[str]]
    type: Literal["object"]


class AnnotationsOutputSchema(TypedDict):
    properties: NotRequired[OutputSchemaProperties]
    required: NotRequired[list[str]]
    type: Literal["object"]


class AnnotationsTool(TypedDict):
    _meta: NotRequired[ToolMeta]
    annotations: NotRequired[ToolAnnotations]
    description: NotRequired[str]
    input_schema: Annotated[AnnotationsInputSchema, Field(alias="inputSchema")]
    name: str
    output_schema: Annotated[NotRequired[AnnotationsOutputSchema], Field(alias="outputSchema")]
    title: NotRequired[str]


class AnnotationsToolAnnotations(TypedDict):
    destructive_hint: Annotated[NotRequired[bool], Field(alias="destructiveHint")]
    idempotent_hint: Annotated[NotRequired[bool], Field(alias="idempotentHint")]
    open_world_hint: Annotated[NotRequired[bool], Field(alias="openWorldHint")]
    read_only_hint: Annotated[NotRequired[bool], Field(alias="readOnlyHint")]
    title: NotRequired[str]


@with_config(extra="allow")
class ToolListChangedNotificationParams(TypedDict):
    _meta: NotRequired[ParamsMeta]


class AnnotationsToolListChangedNotification(TypedDict):
    method: Literal["notifications/tools/list_changed"]
    params: NotRequired[ToolListChangedNotificationParams]


class UnsubscribeRequestParams(TypedDict):
    uri: str


class AnnotationsUnsubscribeRequest(TypedDict):
    method: Literal["resources/unsubscribe"]
    params: UnsubscribeRequestParams
