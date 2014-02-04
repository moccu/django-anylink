window.AnyLinkAddOrChangeWidget = {
	show: function(el) {
		var name = el.id.replace(/^lookup_/, ''),
			value = document.getElementById(name).value,
			window_name = name.replace(/\./g, '__dot__').replace(/\-/g, '__dash__'),
			href = el.href.split('?'),
			url = href[0],
			params, win;

		if (href.length > 1) {
			params = href.slice(1).join('?') + '&_popup=1&aoc=1';
		} else {
			params = '_popup=1&aoc=1';
		}

		if (!value) {
			value = 'add';
		}

		win = window.open(url + value + '/?' + params, window_name,
			'height=500,width=800,resizable=yes,scrollbars=yes');

		win.focus();
		return false;
	},

	delete: function(delete_element) {
		var name = delete_element.id.replace(/^delete_/, ''),
			input = document.getElementById(name),
			lookup_element = document.getElementById('lookup_' + name),
			name_element = document.getElementById('name_' + name)

		input.value = '';
		lookup_element.innerHTML = lookup_element.getAttribute('data-add');
		name_element.innerHTML = '';
		delete_element.style.display = 'none';

		return false;
	},

	callback: function (win, link_id, link_name) {
		var name = win.name.replace(/__dot__/g, '.').replace(/__dash__/g, '-'),
			input = document.getElementById(name),
			lookup_element = document.getElementById('lookup_' + name),
			name_element = document.getElementById('name_' + name),
			delete_element = document.getElementById('delete_' + name);

		input.value = link_id;
		lookup_element.innerHTML = lookup_element.getAttribute('data-change');
		// TODO: Check if name element was found, if not, create one.
		name_element.innerHTML = link_name
		delete_element.style.display = 'inline';

		win.close();
	}
};
