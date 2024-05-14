import api from '../components/api';

const handleSendMessage = async (
    e, currentMessage, fortniteStats, chatMessages, setChatMessages, setCurrentMessage
) => {
    e.preventDefault();
    if (!currentMessage.trim()) return;

    const userMessage = { sender: 'User', text: currentMessage };
    setChatMessages([...chatMessages, userMessage]);

    try {
        const response = await api.post('/chatbot', { message: currentMessage, fortniteStats });
        const botMessage = { sender: 'Bot', text: response.data.response };
        setChatMessages([...chatMessages, botMessage]);
    } catch (error) {
        console.error('Error:', error);
    }

    setCurrentMessage('');
};

export default handleSendMessage;
