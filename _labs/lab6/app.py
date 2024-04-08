from vetiver import VetiverModel
import vetiver
import pins


b = pins.board_folder('./model', allow_pickle_read=True)
v = VetiverModel.from_pin(b, 'penguin_model', version = '20230422T102952Z-cb1f9')

vetiver_api = vetiver.VetiverAPI(v)
api = vetiver_api.app
