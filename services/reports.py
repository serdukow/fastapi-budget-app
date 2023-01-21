import csv
from typing import Any
from io import StringIO

from fastapi import Depends

from services.operations import OperationService
from models.operations import OperationCreate, Operation


class ReportsService:
    def __init__(self, operation_service: OperationService = Depends()):
        self.operation_service = operation_service

    def import_csv(self, user_id: int, file: Any):
        reader = csv.DictReader(                          # Информация будет получена в байтах, поэтому ее нужно декодировать
            (line.decode() for line in file),
            fieldnames=[                                  # То какие именно поля мы буде импортировать
                'date',
                'kind',
                'amount',
                'description',
            ]
        )

        operations = []
        next(reader)
        for row in reader:
            operation_data = OperationCreate.parse_obj(row)
            if operation_data.description == '':
                operation_data.description = None
            operations.append(operation_data)

        self.operation_service.create_many(
            user_id,
            operations
        )

    def export_csv(self, user_id: int) -> Any:
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=[  # То какие именно поля мы буде импортировать
                'date',
                'kind',
                'amount',
                'description',
            ],
            extrasaction='ignore',      # Если будет передаваться больше полей, чем в fieldnames, то writer будет их игнорить
        )

        operations = self.operation_service.get_list(user_id)

        writer.writeheader()
        for operation in operations:
            operation_data = Operation.from_orm(operation)
            writer.writerow(operation_data.dict())

            output.seek(0)
            return output




