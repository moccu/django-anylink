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
			'height=710,width=980,resizable=yes,scrollbars=yes');

		win.focus();
		return false;
	},

	select: function(el) {
		var name = el.id.replace(/^lookup_/, ''),
			window_name = name.replace(/\./g, '__dot__').replace(/\-/g, '__dash__'),
			href = el.href.split('?'),
			url = href[0],
			params, win;

		if (href.length > 1) {
			params = href.slice(1).join('?') + '&_popup=1';
		} else {
			params = '_popup=1';
		}

		win = window.open(url + '?' + params, window_name,
			'height=710,width=980,resizable=yes,scrollbars=yes');

		win.addEventListener('DOMContentLoaded', function () {
			var $ = win.django.jQuery;

			$('table#result_list tbody tr th a')
				.attr('onclick', '')
				.click(function(e) {
					e.preventDefault();
					var $this = $(this),
						link_id = $this.attr('href').match(/anylink\/(\d+)\//);

					if (link_id) {
						window.AnyLinkAddOrChangeWidget.callback(
							win, link_id[1], $this.text());
					}
				});
		});

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
