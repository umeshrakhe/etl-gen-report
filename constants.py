from enum import Enum


class DBType(Enum):
    """Database type enumeration."""
    ORACLE = "oracle"
    MYSQL = "mysql"
    POSTGRES = "postgres"
    SQLSERVER = "sqlserver"
    DB2 = "db2"


class ExitCodes(Enum):
    """Program return code enumeration."""
    SUCCESS = 0
    GENERIC_ERROR = 1
    DATABASE_ERROR = 3  # value 2 is reserved for wrong arguments passed via argparse
    DATA_LOADING_ERROR = 4


class TerminalColor(Enum):
    GREEN = "\x1b[32m"
    RED = "\x1b[31m"
    YELLOW = "\x1b[33m"
    RESET = "\x1b[0m"


class DBConfigKeys(str, Enum):
    IDENTIFIER_QUOTE = "identifier_quote"


DBConfig = {
    DBConfigKeys.IDENTIFIER_QUOTE: {
        DBType.MYSQL:     "`",
        DBType.ORACLE:    '"',
        DBType.POSTGRES:  '"',
        DBType.SQLSERVER: '"',
        DBType.DB2:       '"'
    }
}