from enum import Enum

class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED="file type not supported"
    FILE_TYPE_EXCEEDED="file size exceeded"
    FILE_UPLOADED_SUCCESS="success"
    FILE_UPLOADED_FAILED="file uploaded failed"
    FILE_VALIDATED_SUCCESS="file validated successfully"
    FILE_PROCESSING_FAILED="file processing failed"
    FILE_PROCESSING_SUCCESS="file processed successfully"
    NO_FILE_ERROR="not found file "
    FILE_ID_ERROR="no file found with this id"
    PROJECT_NOT_FOUND_ERROR="project not found"
    INSERT_INTO_VRCTORDB_ERROR="failed to insert into vector db"
    INSERT_INTO_VECTORDB_SUCCESS="successfully inserted into vector db"
    VECTORDB_COLLECTION_RETRIEVED="successfully retrieved vector db collection info"
    VECTOR_SEARCH_ERROR="failed to search in vector db collection"
    VECTOR_SEARCH_SUCCESS="successfully searched in vector db collection"
