from asin_update_prog import *

main_inst = Asin_update()
main_inst.cat_update_inst.start()
main_inst.amazon_inst.start()
while True:
	main_inst.get_ids("id_to_check")
	if main_inst.get_id_queue():
		#if id_queue is not empty
		main_inst.mov_ids()
		main_inst.get_descriptions()
		main_inst.create_asins()
		#need to make 
		main_inst.get_asins()
		main_inst.delete_bcodes()
		main_inst.update_asins()
		main_inst.set_asin_id_lst([])






