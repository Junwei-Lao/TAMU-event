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
          introMessage={{text: 'Plese put down what events you want to know about. It can be long or short. We will try our best to help you! \n \n To see what extra functions we have, type **/commands** \n \n To report any issues, please send message to **report@tamuevent.com** \n \n Unlike other websites that keep message history, your message will be cleared once you refresh'}}
          connect={{
            url: 'http://localhost:6500/chat',
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
          }}
          requestBodyLimits={{maxMessages: -1}}
          requestInterceptor={(details: RequestDetails) => {
            console.log(details);
            return details;
          }}
          responseInterceptor={(response: any) => {
            console.log(response);
            return response;
          }}
        />
      </div>
    </div>
  );
}

export default App;