from vetiver import VetiverModel
import vetiver
import pins


b = pins.board_folder('/var/folders/t9/kw5hnztj68d6_37dm5rw8n_h0000gn/T/tmpti3uqb2x', allow_pickle_read=True)
v = VetiverModel.from_pin(b, 'penguin_model')

vetiver_api = vetiver.VetiverAPI(v)
api = vetiver_api.app
