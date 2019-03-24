from DataServiceFile import IDataService, TextDataService, DBDataService


class MainClass():

    def __init__(self, data_service):
        if not isinstance(data_service, IDataService):
            raise RuntimeError("data_service must be an IDataService interface")
        self.data_service = data_service
        pass

    def on_message_recived(self, message, client_id):
        history = self.data_service.get_history(client_id)
        print(history)
        # answer = self.create_answer(message, history)
        # self.data_service.save_message(client_message=message, bot_answer=answer, client_id=client_id)
        pass


if __name__ == '__main__':
    pass
    # do cool things