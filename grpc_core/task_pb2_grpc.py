# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import task_pb2 as task__pb2


class TaskStub(object):
    """Task
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.New = channel.unary_unary(
                '/jijidown.core.Task/New',
                request_serializer=task__pb2.TaskNewReq.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.NewBatch = channel.unary_unary(
                '/jijidown.core.Task/NewBatch',
                request_serializer=task__pb2.TaskNewBatchReq.SerializeToString,
                response_deserializer=task__pb2.TaskNewBatchReply.FromString,
                )
        self.Status = channel.unary_unary(
                '/jijidown.core.Task/Status',
                request_serializer=task__pb2.TaskStatusReq.SerializeToString,
                response_deserializer=task__pb2.TaskStatusReply.FromString,
                )
        self.List = channel.unary_unary(
                '/jijidown.core.Task/List',
                request_serializer=task__pb2.TaskListReq.SerializeToString,
                response_deserializer=task__pb2.TaskListReply.FromString,
                )
        self.Control = channel.unary_unary(
                '/jijidown.core.Task/Control',
                request_serializer=task__pb2.TaskControlReq.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.Notification = channel.unary_stream(
                '/jijidown.core.Task/Notification',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=task__pb2.TaskNotificationReply.FromString,
                )


class TaskServicer(object):
    """Task
    """

    def New(self, request, context):
        """创建新任务
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def NewBatch(self, request, context):
        """批量创建新任务
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Status(self, request, context):
        """任务状态
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def List(self, request, context):
        """获取任务列表
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Control(self, request, context):
        """任务控制 (暂停, 继续, 删除)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Notification(self, request, context):
        """任务完成通知
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TaskServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'New': grpc.unary_unary_rpc_method_handler(
                    servicer.New,
                    request_deserializer=task__pb2.TaskNewReq.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'NewBatch': grpc.unary_unary_rpc_method_handler(
                    servicer.NewBatch,
                    request_deserializer=task__pb2.TaskNewBatchReq.FromString,
                    response_serializer=task__pb2.TaskNewBatchReply.SerializeToString,
            ),
            'Status': grpc.unary_unary_rpc_method_handler(
                    servicer.Status,
                    request_deserializer=task__pb2.TaskStatusReq.FromString,
                    response_serializer=task__pb2.TaskStatusReply.SerializeToString,
            ),
            'List': grpc.unary_unary_rpc_method_handler(
                    servicer.List,
                    request_deserializer=task__pb2.TaskListReq.FromString,
                    response_serializer=task__pb2.TaskListReply.SerializeToString,
            ),
            'Control': grpc.unary_unary_rpc_method_handler(
                    servicer.Control,
                    request_deserializer=task__pb2.TaskControlReq.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'Notification': grpc.unary_stream_rpc_method_handler(
                    servicer.Notification,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=task__pb2.TaskNotificationReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'jijidown.core.Task', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Task(object):
    """Task
    """

    @staticmethod
    def New(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jijidown.core.Task/New',
            task__pb2.TaskNewReq.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def NewBatch(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jijidown.core.Task/NewBatch',
            task__pb2.TaskNewBatchReq.SerializeToString,
            task__pb2.TaskNewBatchReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Status(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jijidown.core.Task/Status',
            task__pb2.TaskStatusReq.SerializeToString,
            task__pb2.TaskStatusReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def List(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jijidown.core.Task/List',
            task__pb2.TaskListReq.SerializeToString,
            task__pb2.TaskListReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Control(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jijidown.core.Task/Control',
            task__pb2.TaskControlReq.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Notification(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/jijidown.core.Task/Notification',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            task__pb2.TaskNotificationReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)