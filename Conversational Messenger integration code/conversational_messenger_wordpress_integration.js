/*
 * Outside of WordPress context, nest inside an appropriate <body> tag in an HTML file.
 * ToDo: add blog post title & URL 
 */

<script>
  // Debugging: Log the current page URL to check for accuracy
  console.log("Current URL:", window.location.href);

  // Check if the current URL matches either page 4903 or 5051 (partial match for robustness)
  if (window.location.href.includes("?p=4903") || window.location.href.includes("?p=5051")) {
    console.log("Widget will be added to this page");

    // Set a delay of 1 second to show the chatbot
    setTimeout(() => {
      // Inject Dialogflow Messenger widget only after the delay
      const head = document.head;

      // Add stylesheet
      const stylesheet = document.createElement("link");
      stylesheet.rel = "stylesheet";
      stylesheet.href = "https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/themes/df-messenger-default.css";
      head.appendChild(stylesheet);

      // Add Roboto font
      const font = document.createElement("link");
      font.rel = "stylesheet";
      font.href = "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap";
      head.appendChild(font);

      // Add Dialogflow script
      const script = document.createElement("script");
      script.src = "https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/df-messenger.js";
      script.onload = () => {
        console.log("Dialogflow script loaded successfully");

        // Add the widget HTML
        const widgetHTML = `
          <df-messenger
            project-id="fooctrl-REDACTED"
            agent-id="REDACTED"
            language-code="en"
            max-query-length="-1"
            allow-feedback="all"
            session-ttl="1800">
            <df-messenger-chat-bubble
              chat-title="auto-cpufreq genAI chatbot"
              minimized="false"
              expanded="true"
              chat-icon="https://storage.googleapis.com/foolcontrol-media/2025/01/4ca21334-icon.png"
              chat-close-icon="https://storage.googleapis.com/foolcontrol-media/2025/01/4ca21334-icon.png">
            </df-messenger-chat-bubble>
          </df-messenger>
          <style>
            df-messenger {
              z-index: 999;
              position: fixed;
              font-family: 'Roboto', sans-serif;
              --df-messenger-font-color: #000;
              --df-messenger-chat-background: #E7EFFE;
              --df-messenger-message-user-background: #C6DAFC;
              --df-messenger-message-bot-background: #C8E6C9;
              bottom: 16px;
              right: 16px;
              opacity: 0; /* Start with 0 opacity for effect */
              transform: scale(0.5); /* Start smaller */
              animation: genieEffect 1s forwards; /* Apply the genie effect animation */
            }
            df-messenger-chat-bubble {
              width: 100%;
              height: auto;
            }

            /* Keyframe animation for the genie effect */
            @keyframes genieEffect {
              0% {
                opacity: 0;
                transform: scale(0.5) translateY(20px); /* Start small and lower */
              }
              100% {
                opacity: 1;
                transform: scale(1) translateY(0); /* End at normal size and position */
              }
            }
          </style>`;
        document.body.insertAdjacentHTML("beforeend", widgetHTML);

        // Function to set the width and height of the chat bubble based on the screen size
        function updateChatBubbleSize() {
          const chatBubble = document.querySelector('df-messenger-chat-bubble');

          if (window.innerWidth >= 768) {  // Desktop size (768px and above)
            chatBubble.setAttribute('chat-width', '600');
            chatBubble.setAttribute('chat-height', '700');
          } else {  // Mobile size
            chatBubble.setAttribute('chat-width', '100%');
            chatBubble.setAttribute('chat-height', 'auto');
          }
        }

        // Initial update when the page loads
        updateChatBubbleSize();

        // Update the chat bubble size on window resize
        window.addEventListener('resize', updateChatBubbleSize);
      };

      script.onerror = () => {
        console.error("Failed to load Dialogflow script");
      };

      head.appendChild(script);

    }, 1000); // 1000ms = 1 second

  } else {
    console.log("Widget will not be added to this page");
  }
</script>
