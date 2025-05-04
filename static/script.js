document.addEventListener('DOMContentLoaded', function() {
    const chatArea = document.getElementById('chatArea');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const bookingsList = document.getElementById('bookingsList');
    
    // Generate unique user ID
    const userId = 'user-' + Math.random().toString(36).substr(2, 9);
    
    // Initial greeting
    addBotMessage("Hello! I'm your IRCTC assistant. How can I help you today?");
    
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendMessage();
    });
    
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;
        
        addUserMessage(message);
        userInput.value = '';
        
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: userId,
                message: message
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                addBotMessage("Sorry, something went wrong. Please try again.");
                console.error(data.error);
            } else {
                addBotMessage(data.response);
                updateBookings(data.bookings);
            }
        });
    }
    
    function addUserMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        messageDiv.textContent = text;
        chatArea.appendChild(messageDiv);
        chatArea.scrollTop = chatArea.scrollHeight;
    }
    
    function addBotMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.textContent = text;
        chatArea.appendChild(messageDiv);
        chatArea.scrollTop = chatArea.scrollHeight;
    }
    
    function updateBookings(bookings) {
        bookingsList.innerHTML = '';
        if (bookings.length === 0) {
            bookingsList.innerHTML = '<p>No bookings yet</p>';
            return;
        }
        
        bookings.forEach(booking => {
            const card = document.createElement('div');
            card.className = 'booking-card';
            card.innerHTML = `
                <h3>Booking ${booking.id}</h3>
                <p>${booking.details}</p>
                <small>${new Date(booking.timestamp).toLocaleString()}</small>
            `;
            bookingsList.appendChild(card);
        });
    }
});