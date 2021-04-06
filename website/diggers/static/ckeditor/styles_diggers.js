/**
 * Copyright (c) 2003-2021, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-oss-license
 */

// This file contains style definitions that can be used by CKEditor plugins.
//
// The most common use for it is the "stylescombo" plugin which shows the Styles drop-down
// list containing all styles in the editor toolbar. Other plugins, like
// the "div" plugin, use a subset of the styles for their features.
//
// If you do not have plugins that depend on this file in your editor build, you can simply
// ignore it. Otherwise it is strongly recommended to customize this file to match your
// website requirements and design properly.
//
// For more information refer to: https://ckeditor.com/docs/ckeditor4/latest/guide/dev_styles.html#style-rules

CKEDITOR.stylesSet.add( 'diggers', [
	/* Block styles */

	{ name: 'Аббривеатури',		element: 'abbr' },
	{ name: 'Маркований',		element: 'mark' },
	{ name: 'Код', 			element: 'code' },
	{ name: 'Маленький',	element: 'small' },
	{ name: 'Буквиця', 		element: 'p', attributes: { class: 'drop-cap' } },
	{ name: 'Виділений абзац', 		element: 'p', attributes: { class: 'lead' } },

	{ name: 'Жирний',			element: 'strong', overrides: 'b' },
	{ name: 'Курсив',			element: 'em'	, overrides: 'i' },
	{ name: 'Підкреслений',		element: 'u' },
	{ name: 'Закреслений',		element: 'del', overrides: 's'  },

	/* Object styles */

	{
		name: 'Обтікання зображення зліва',
		element: 'img',
		attributes: { 'class': 'h-pull-left' }
	},

	{
		name: 'Обтікання зображення зправа',
		element: 'img',
		attributes: { 'class': 'h-pull-right' }
	},

	/* Widget styles */
	{ name: '240p', type: 'widget', widget: 'embedSemantic', attributes: { 'class': 'video-container' }, group: 'size' },
	{ name: '360p', type: 'widget', widget: 'embedSemantic', attributes: { 'class': 'video-container' }, group: 'size' },
	{ name: '480p', type: 'widget', widget: 'embedSemantic', attributes: { 'class': 'video-container' }, group: 'size' },
	{ name: '720p', type: 'widget', widget: 'embedSemantic', attributes: { 'class': 'video-container' }, group: 'size' },
	{ name: '1080p', type: 'widget', widget: 'embedSemantic', attributes: { 'class': 'video-container' }, group: 'size' },

	// Adding space after the style name is an intended workaround. For now, there
	// is no option to create two styles with the same name for different widget types. See https://dev.ckeditor.com/ticket/16664.
	{ name: '240p ', type: 'widget', widget: 'embed', attributes: { 'class': 'video-container' }, group: 'size' },
	{ name: '360p ', type: 'widget', widget: 'embed', attributes: { 'class': 'video-container' }, group: 'size' },
	{ name: '480p ', type: 'widget', widget: 'embed', attributes: { 'class': 'video-container' }, group: 'size' },
	{ name: '720p ', type: 'widget', widget: 'embed', attributes: { 'class': 'video-container' }, group: 'size' },
	{ name: '1080p ', type: 'widget', widget: 'embed', attributes: { 'class': 'video-container' }, group: 'size' }

] );

