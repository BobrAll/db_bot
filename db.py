def load_addresses():
	# load from db
	return ['Адрес 1', 'Адрес 2', 'Адрес 3']


def load_storages(store_address):
	# return loaded from db storages id's
	return ['склад_1', 'склад_2']


def load_providers(store_address):
	# return loaded from db providers
	return ['поставщик_1', 'поставщик_2']


def show_storage_items_info(id):
	return ("Хранимые предметы: "
	        "\n..."
	        "\n..."
	        "\n...")
	# return info from db about storage items


def show_storage_machines_info(id):
	return ("Используемое оборудование: "
	        "\n..."
	        "\n..."
	        "\n...")
	# return info from db about storage machines

def get_titles_list(address):
	return ['Шоколад Аленка', 'Вода Святой источник']

def make_oder(address, order):
	#add needed titles in db
    pass
