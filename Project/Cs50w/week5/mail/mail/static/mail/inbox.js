// When back arrow is clicked, show previous mailbox
// window.onpopstate = function (event) {
// 	if (event.state.mailbox) {
// 		load_mailbox(event.state.mailbox)
// 	} else if (!event.state) {
// 		compose_email()
// 	} else {
// 		load_email(event.state.mail)
// 	}
// }

document.addEventListener('DOMContentLoaded', function () {

	// Use buttons to toggle between views
	buttons = document.querySelectorAll('#navigations button')
	buttons.forEach(button => button.addEventListener('click', () => {
		if (button.innerHTML == "Compose") {
			// Update the URL
			// history.pushState({}, "", "compose")
			compose_email()
		} else {
			// Update the URL
			mailbox = button.id
			// history.pushState({ mailbox: mailbox }, "", `${mailbox}`)
			load_mailbox(`${mailbox}`)
		}
	}))
	load_mailbox('inbox');
});

function compose_email() {

	// Show compose view and hide other views
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#email-view').style.display = 'none';
	document.querySelector('#compose-view').style.display = 'block';

	// Clear out composition fields
	document.querySelector('#compose-recipients').value = '';
	document.querySelector('#compose-subject').value = '';
	document.querySelector('#compose-body').value = '';
}


function load_mailbox(mailbox) {

	// Show the mailbox and hide other views
	document.querySelector('#emails-view').style.display = 'block';
	document.querySelector('#email-view').style.display = 'none';
	document.querySelector('#compose-view').style.display = 'none';

	// Show the mailbox name
	emailsView = document.querySelector('#emails-view')
	emailsView.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

	// Load the appropriate mailbox
	fetch(`emails/${mailbox}`)
		.then(response => response.json())
		.then(data => data.forEach(e => {
			// create div for each email			
			div = document.createElement('div')
			div.setAttribute('data-id', `${e.id}`)
			if (e.read) {
				div.className = "mail read"
			} else {
				div.className = "mail unread"
			}
			div.addEventListener('click', () => {
				// history.pushState({ mail: e.id }, '', `mail${e.id}`)
				load_email(e.id)
			})
			
			// append infomation of the email
			sender = e.sender
			subject = e.subject
			timestamp = e.timestamp
			div.innerHTML = `<div>${sender}</div><div>${subject}</div><div>${timestamp}</div>`
			emailsView.appendChild(div)		
		})
		)
}

// sent email
document.addEventListener('DOMContentLoaded', function () {
	form = document.querySelector('#compose-form')
	form.onsubmit = () => {
		fetch('/emails', {
			method: 'POST',
			body: JSON.stringify({
				recipients: document.querySelector('#compose-recipients').value,
				subject: document.querySelector('#compose-subject').value,
				body: document.querySelector('#compose-body').value
			})
		})
			.then(response => response.json())
			.then(result => {
				// Print result
				if (result.message) {
					alert(result.message)
					load_mailbox('sent')
				} else {
					alert(result.error)
				}
			})
		return false
	}
})

function load_email(email_id) {
	//  Show the email and hide other views
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#email-view').style.display = 'flex';
	document.querySelector('#compose-view').style.display = 'none';

	fetch(`/emails/${email_id}`)
		.then(reponse => reponse.json())
		.then(data => {
			document.querySelector('#email-view').innerHTML = ''
			content = [
				{from: `From: ${data.sender}`}, 
				{to: `To: ${data.recipients}`}, 
				{subject: data.subject}, 
				{time: data.timestamp}, 
				{body: data.body.replace(/\n/g, '<br>')}
			]
			content.forEach(e => {
				div = document.createElement('div')
				div.innerHTML = Object.values(e)
				div.setAttribute('id', Object.keys(e))
				document.querySelector('#email-view').appendChild(div)
				// If email is unread, set email as read  
				if (!data.read) {
					fetch(`/emails/${email_id}`, {
						method: 'PUT',
						body: JSON.stringify({
							read: true
						})
					})
				}
			})
			// create archive button on inbox view
			if (!data.archived) {
				a_button = document.createElement('button')
				a_button.innerHTML = "Archive"
				a_button.className = "button archive"
				a_button.addEventListener('click', () => {archive(data.id, "True")})
				document.querySelector('#email-view').appendChild(a_button)
			} else {
				console.log(data.archived)
				ua_button = document.createElement('button')
				ua_button.innerHTML = "Un-archive"
				ua_button.className = "button archive"
				ua_button.addEventListener('click', () => {archive(data.id, "False")})
				document.querySelector('#email-view').appendChild(ua_button)
			}

			// create unarchive button in archived view
				
			// reply button
			button = document.createElement("button")
			button.innerHTML = "Reply"
			button.className = "button reply"
			button.addEventListener('click', () => {
				compose_email()
				// prefill recipients
				document.querySelector('#compose-recipients').value = data.sender
				
				// prefill subject
				subject = document.querySelector('#compose-subject')
				if (data.subject.substr(0,3) === 'Re:') {
					subject.value = `${data.subject}`
				} else {
					subject.value = `Re: ${data.subject}`
				}

				// prefill body
				document.querySelector('#compose-body').value = `\n \n------On ${data.timestamp} ${data.sender} wrote: \n"${data.body}"\n `
			})
			document.querySelector('#email-view').appendChild(button)
		})
}

function archive(email_id, bool) {
	fetch(`/emails/${email_id}`, {
		method: 'PUT',
		body: JSON.stringify({
			archived: `${bool}`
		})
	})
	.then(() => {
		load_mailbox("inbox")
		// history.pushState({ mailbox: 'inbox' }, "", 'inbox')
	})
}
