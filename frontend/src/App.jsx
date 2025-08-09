import { useStytch } from '@stytch/react';
import { StytchLogin, IdentityProvider, useStytchUser } from '@stytch/react';

//to ask the user to login, or if already, to give us consent to their data
function App() {
  
  const {user: User} = useStytchUser();

  const config = {
    "products": [
      "oauth", 
      "passwords"
    ],
    "oauthOptions": {
      "providers": [
        {
          "type": "google"
        },
        {
          "type": "facebook"
        }
      ],
      "loginRedirectURL": "https://www.stytch.com/login",
      "signupRedirectURL": "https://www.stytch.com/signup"
    },
    "emailMagicLinksOptions": {
      "loginRedirectURL": "https://www.stytch.com/login",
      "loginExpirationMinutes": 30,
      "signupRedirectURL": "https://www.stytch.com/signup",
      "signupExpirationMinutes": 30
    },
    "otpOptions": {
      "methods": [],
      "expirationMinutes": 5
    },
    "passwordOptions": {
      "loginRedirectURL": "https://www.stytch.com/login",
      "resetPasswordRedirectURL": "https://www.stytch.com/reset-password"
    }
  }

  return (
    <div style={{display: "flex", justifyContent: "center", alignItems: "center", height: "100vh", width: "100vw"}}>
      <div>
        {!User ? (
          <StytchLogin config = {config} />
        ) : (
          <IdentityProvider />
        )}
      </div>
    </div>
  )
}

export default App

//On Stytch Dashboard, can go to Frontend SDK in menu > click on Javascript SDK > then go back to menu to click configuration playground under frontend sdk to play with different themes, etc and then copy code