document.addEventListener('DOMContentLoaded', () => {
	const authButton = document.querySelector('#auth-button');
	if (!authButton) {
		throw 'DOMContentLoaded: #auth-button not found';
	}
	authButton.addEventListener('click', authButtonClick);

	const itemsButton = document.querySelector('#items-button');
	if (!itemsButton) {
		throw 'DOMContentLoaded: #items-button not found';
	}
	itemsButton.addEventListener('click', itemsButtonClick);
});

const authButtonClick = () => {
	const login = document.querySelector('#login');
	if (!login) {
		throw 'authButtonClick: #login not found';
	}

	const password = document.querySelector('#password');
	if (!password) {
		throw 'authButtonClick: #password not found';
	}

	const credentials = btoa(login.value + ':' + password.value);

	const output = document.querySelector('#output');
	if (!output) {
		throw 'authButtonClick: #output not found';
	}

	fetch('/auth', {
		method: 'GET',
		headers: {
			Authorization: `Basic ${credentials}`
		}
	}).then(r => {
		switch (r.status) {
			case 401:
				r.text().then(text => (output.innerText = text));
				break;
			case 200:
				r.json().then(json => {
					output.innerText = json.token;
					window.sessionStorage.setItem('access_token', json.token);
				});
				break;
		}
	});
};

const itemsButtonClick = () => {
	const accessToken = window.sessionStorage.getItem('access_token');
	if (!accessToken) {
		alert('Authorization required');
		return;
	}

	fetch('/items', {
		method: 'GET',
		headers: {
			Authorization: `Bearer ${accessToken}`
		}
	}).then(r => {
		if (r.status != 200) {
			output.innerText = 'Content is blocked';
		} else {
			output.innerText = 'Content will be here';
		}
	});
};
