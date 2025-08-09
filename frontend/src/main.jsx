import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import { StytchProvider } from '@stytch/react';
import { createStytchUIClient } from '@stytch/react/ui';


import './index.css'
import App from './App.jsx'

const stytch = createStytchUIClient('public-token-test-11d57201-b8d0-42a4-bfbb-fd19c7935421');

//wrapping the app in the stytch provider, so all components have access to the stytch client
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <StytchProvider stytch={stytch}>
      <App />
    </StytchProvider>
  </StrictMode>,
)

//copying over some code from example usage of stytch react sdk: https://www.npmjs.com/package/@stytch/react?activeTab=readme