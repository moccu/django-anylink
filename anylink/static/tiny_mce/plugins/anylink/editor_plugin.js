(function() {
	tinymce.PluginManager.requireLangPack('anylink');

	var plugin = {
		init : function(ed, url) {

			// Private functions
			var getAnyLinkId = function(editor) {
				var node = editor.selection.getNode();
				var tagname = node.tagName.toLowerCase();

				if(tagname === 'a') {
					var hrefAttribute = node.getAttributeNode('href');
					if( hrefAttribute && hrefAttribute.nodeValue.substring(0, 3) === '#AL') {
						return hrefAttribute.nodeValue.substring(3);
					}
				}

				return '';
			}

			// Public functions
			tinymce.plugins.AnyLink.popupCallback = function(editorId, linkId) {
				var editor = tinymce.getInstanceById(editorId);

				if (editor != null) {
					var node = editor.selection.getNode();
					var tagname = node.tagName.toLowerCase();

					if(tagname !== 'a') {
						// No link. Wrap current content.
						var text = editor.selection.getContent({format: 'raw'});
						var link = '<a href="' + linkId + '">' + text + '</a>';
						editor.selection.setContent(link);
					} else {
						// Link exists, remove all attributes
						var attrs = node.attributes;
						for(var i=0; i < attrs.length; i++) {
							node.removeAttributeNode(attrs[i]);
						}

						// .. and add href attribute.
						var href_attribute = document.createAttribute('href');
						href_attribute.nodeValue = linkId;
						node.setAttributeNode(href_attribute);
					}
				}
			}

			// Commands
			ed.addCommand('mceAnyLinkAdd', function() {
				var anylink_id = getAnyLinkId(ed);
				if (!anylink_id) { anylink_id = 'add'; }

				ed.windowManager.open({
					file : tinyMCE.settings.anylink_url + anylink_id + '/?ed=' + ed.id + '&_popup=1',
					width : 980,
					height : 710,
					inline : 1
				}, {
					plugin_url : url,
					editor : ed.id
				});
			});

			// Buttons
			ed.addButton('anylink', {
				title: 'anylink.descAddAnyLink',
				cmd: 'mceAnyLinkAdd',
				image: url + '/img/link.gif'
			});

			// Events
			ed.onNodeChange.add(function(ed, cm, n) {
				if (n) {
					var tagname = n.tagName.toLowerCase();
					var selection = ed.selection.getContent({format: 'raw'});

					cm.setActive('anylink', false);
					if( selection !== '' || tagname === 'a' ) {
						cm.setDisabled('anylink', false);
						if (tagname === 'a') {
							cm.setActive('anylink', true);
						}
					} else {
						cm.setDisabled('anylink', true);
					}
				}
			});
		},

		// Plugin info
		getInfo : function() {
			return {
				longname : 'AnyLink Plugin',
				author : 'Moccu GmbH & Co KG',
				authorurl : 'http://www.moccu.com',
				infourl : '',
				version : '0.0.1'
			};
		}
	};

	tinymce.create('tinymce.plugins.AnyLink', plugin);
	tinymce.PluginManager.add('anylink', tinymce.plugins.AnyLink);
})();
