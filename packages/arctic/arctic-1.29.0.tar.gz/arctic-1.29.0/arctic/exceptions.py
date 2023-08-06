class ArcticException(Exception):
    pass


class NoDataFoundException(ArcticException):
    pass


class UnhandledDtypeException(ArcticException):
    pass


class LibraryNotFoundException(ArcticException):
    pass


class DuplicateSnapshotException(ArcticException):
    pass


class StoreNotInitializedException(ArcticException):
    pass


class OptimisticLockException(ArcticException):
    pass


class ConcurrentModificationException(ArcticException):
    pass


class QuotaExceededException(ArcticException):
    pass


class UnorderedDataException(ArcticException):
    pass


class OverlappingDataException(ArcticException):
    pass


class UnsupportedPickleStoreVersion(ArcticException):
    pass
