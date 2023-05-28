{
    "name": "Sync Deta",
    "summary": "Base mo",
    "author": "Thinh Luu",
    "category": "Tools",
    "version": "15.0.0.0.1",    
    "license": "AGPL-3",
    "external_dependencies": {"python": ["deta","dotty-dict"]},    
    "depends": ["base", "web"],
    "installable": True,

    'data': [
        'views/res_config_setting_views.xml',
    ],

    "assets": {
        "web.assets_backend": [
            'sync_deta/static/src/js/widget_sync_deta.js',
        ],
    },
}
