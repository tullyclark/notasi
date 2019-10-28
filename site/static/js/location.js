
fields = [{
	"type": "none",
	"fields": [{
		"id": "address",
		"display": "hide"
	}, {
		"id": "port",
		"display": "hide",
	}, {
		"id": "database",
		"display": "hide"
	}, {
		"id": "username",
		"display": "hide"
	}, {
		"id": "password",
		"display": "hide"
	}, {
		"id": "subtype_id",
		"display": "hide"
	}]
}, {
	"type": "Folder",
	"fields": [{
		"id": "address",
		"display": "show",
		"label": "Folder",
		"placeholder": "Folder"
	}, {
		"id": "port",
		"display": "hide",
	}, {
		"id": "database",
		"display": "hide"
	}, {
		"id": "username",
		"display": "hide"
	}, {
		"id": "password",
		"display": "hide"
	}, {
		"id": "subtype_id",
		"display": "hide"
	}]
}, {
	"type": "Notasi Groups",
	"fields": [{
		"id": "address",
		"display": "hide"
	}, {
		"id": "port",
		"display": "hide",
	}, {
		"id": "database",
		"display": "hide"
	}, {
		"id": "username",
		"display": "hide"
	}, {
		"id": "password",
		"display": "hide"
	}, {
		"id": "subtype_id",
		"display": "hide"
	}]
}, {
	"type": "Notasi Users",
	"fields": [{
		"id": "address",
		"display": "hide"
	}, {
		"id": "port",
		"display": "hide",
	}, {
		"id": "database",
		"display": "hide"
	}, {
		"id": "username",
		"display": "hide"
	}, {
		"id": "password",
		"display": "hide"
	}, {
		"id": "subtype_id",
		"display": "hide"
	}]
}, {
	"type": "LDAP",
	"fields": [{
		"id": "address",
		"display": "show",
		"label": "Address",
		"placeholder": "ldaps://..."
	}, {
		"id": "port",
		"display": "hide",
	}, {
		"id": "database",
		"display": "show",
		"label": "Domain",
		"placeholder": "test.nsw.edu.au"
	}, {
		"id": "username",
		"display": "show",
		"label": "Username",
		"placeholder": "Username"
	}, {
		"id": "password",
		"display": "show",
		"label": "Password"
	}, {
		"id": "subtype_id",
		"display": "show"
	}]
}, {
	"type": "SQL",
	"fields": [{
		"id": "address",
		"display": "show",
		"label": "Address",
		"placeholder": "database.test.nsw.edu.au"
	}, {
		"id": "port",
		"display": "show",
	}, {
		"id": "database",
		"display": "show",
		"label": "Database",
		"placeholder": "testdb"
	}, {
		"id": "username",
		"display": "show",
		"label": "Username",
		"placeholder": "Username"
	}, {
		"id": "password",
		"display": "show",
		"label": "Password"
	}, {
		"id": "subtype_id",
		"display": "show"
	}]
}, {
	"type": "HTTP",
	"fields": [{
		"id": "address",
		"display": "show",
		"label": "Address",
		"placeholder": "https://test.nsw.edu.au/api"
	}, {
		"id": "port",
		"display": "hide",
	}, {
		"id": "database",
		"display": "hide"
	}, {
		"id": "username",
		"display": "hide"
	}, {
		"id": "password",
		"display": "hide"
	}, {
		"id": "subtype_id",
		"display": "hide"
	}]
}]











query_view("#location_type_id", "location_type");
$('#location_type_id').change(function(){
	query_view("#location_type_id", "location_type");
});

