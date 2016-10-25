#js function library
#add string variable to document and then to the 

#finds an element by the id
fb_id = '''
		function fb_id(x) {
			var item = document.getElementById(x);
			if (item == null){
				return False;
			}
			else{
				return item;
			}

		}'''
#finds an element by the class namef
fb_cn = '''
		function fb_cn(x){
		var item = document.getElementsByClassName(x);
		if (item == null){
			return False;
			}
		else{
			return item[0]
		}
		}
		'''
#finds elements by class name (returns a list)
fb_cn_m = '''
		function fb_cn_m(x){
		var item = document.getElementsByClassName(x);
		if (item == null){
			return False;
			}
		else{
			return item;
		}
		}
		'''
#finds elements by tag name
fb_tn= '''
	function fb_tn(x){
		var items = document.getElementsByTagName(x);
		return items;
	};'''
#removes an element
rem_e = '''
	function rem_e(x){
		var p_item = x.parentNode;
		p_item.removeChild(x);

		}'''
fb_inner = '''
	function fb_inner(x, target){
	for (i = 0; i < x.length ; i++){
		if (x[i].innerHTML == target) {
			return x[i];

		}
		else{
			return False;
		}
	}
	}'''

js_funcs = [fb_id, fb_cn, fb_cn_m, fb_tn, rem_e, fb_inner]
variables = []
objects = []