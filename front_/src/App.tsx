import {RequestDetails} from 'deep-chat/dist/types/interceptors';
import {DeepChat} from 'deep-chat-react';
import './App.css';

// To see more tutorial materials, visit: https://deepchat.dev/docs/introduction



function App() {
  return (
    <div className="App">
      <div className="components">
        <DeepChat
          className='dc-container'
          style={{width: '98%', height: '93vh'}}
          introMessage={{text: 'Welcome! 👋 \n \n Tell us what events you’re interested in — short or detailed, we’ll do our best to help! We’ll search for up to 20 best-matching events based on what you send us.\n \n 💡 *Try sending: What events related to building a good resume are coming up in the future?* \n \n To explore more features, send **/commands** \n \n To report any issues, contact **junweilao@tamu.edu** \n \n *Note: For your privacy, chat history will be cleared when you refresh the page.* '}}
          connect={{
            url: '/api/chat',
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
          }}
          requestBodyLimits={{maxMessages: -1}}
          requestInterceptor={(detailsToBack: RequestDetails) => {
            console.log(detailsToBack);
            return detailsToBack;
          }}
          responseInterceptor={(responseFromBack: any) => {
            console.log(responseFromBack);
            return responseFromBack;
          }}
        />
      </div>
    </div>
  );
}

export default App;