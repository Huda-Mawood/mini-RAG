from enum import Enum

class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED="file type not supported"
    FILE_TYPE_EXCEEDED="file size exceeded"
    FILE_UPLOADED_SUCCESS="success"
    FILE_UPLOADED_FAILED="file uploaded failed"
    FILE_VALIDATED_SUCCESS="file validated successfully"
    FILE_PROCESSING_FAILED="file processing failed"
    FILE_PROCESSING_SUCCESS="file processed successfully"