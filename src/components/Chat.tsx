import { useEffect, useRef, useState } from "react";
import { FiSend } from "react-icons/fi";
import { BsChevronDown, BsPlusLg } from "react-icons/bs";
import { RxHamburgerMenu } from "react-icons/rx";
import useAnalytics from "@/hooks/useAnalytics";
import useAutoResizeTextArea from "@/hooks/useAutoResizeTextArea";
import Message from "./Message";
import { DEFAULT_OPENAI_MODEL } from "@/shared/Constants";
import * as dotenv from "dotenv";

const Chat = (props: any) => {
  const { toggleComponentVisibility, encodedNumber } = props;

  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [showEmptyChat, setShowEmptyChat] = useState(true);
  const [conversation, setConversation] = useState<any[]>([]);
  // const [conversation, setConversation] = useState<any[]>([
  //   {
  //     content: "what is react",
  //     role: "user",
  //   },
  //   {
  //     content:
  //       "React is a popular JavaScript library for building user interfaces. It was developed by Facebook and is widely used for creating interactive and dynamic web applications. React allows developers to build reusable UI components and efficiently update and render them when the underlying data changes. It follows a component-based architecture, which makes it easier to manage and organize complex user interfaces. React also supports a virtual DOM (Document Object Model) for efficient rendering, making it fast and efficient for creating responsive and interactive web applications.",
  //     role: "system",
  //   },
  // ]);
  const [message, setMessage] = useState("");
  const { trackEvent } = useAnalytics();
  const textAreaRef = useAutoResizeTextArea();
  const bottomOfChatRef = useRef<HTMLDivElement>(null);

  const selectedModel = DEFAULT_OPENAI_MODEL;

  useEffect(() => {
    if (textAreaRef.current) {
      textAreaRef.current.style.height = "24px";
      textAreaRef.current.style.height = `${textAreaRef.current.scrollHeight}px`;
    }
  }, [message, textAreaRef]);

  useEffect(() => {
    if (bottomOfChatRef.current) {
      bottomOfChatRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [conversation]);

  useEffect(() => {
    if (encodedNumber) {
      getWhatsappMessages(encodedNumber);
    }
  }, [encodedNumber]);

  const getWhatsappMessages = async (encodedNumberData: any) => {
    try {
      setIsLoading(true);
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/web-chat-bot/fetch-history`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            number: encodedNumberData,
          }),
        }
      );

      if (response?.status == 200) {
        const data = await response?.json();

        const chatData = data?.data?.conversation?.messages;

        var messages_data = [];
          for (var k = 0; k < chatData?.length; k++) {
            if(k%2==0){
              messages_data.push(chatData[k]);
            }
            else if(k%2 == 1){
              messages_data.push(chatData[k]);
            }
          }
          setConversation(messages_data);
          setIsLoading(false);
          setShowEmptyChat(false);

        // console.log(
        //   "🚀 ~ file: Chat.tsx:98 ~ sendMessage ~ conversation:",
        //   conversation
        // );
      }
    } catch (error: any) {
      console.error(error);
      setErrorMessage(error.message);
    }
  };

  const sendMessage = async (e: any) => {
    e.preventDefault();

    // Don't send empty messages
    if (message.length < 1) {
      setErrorMessage("Please enter a message.");
      return;
    } else {
      setErrorMessage("");
    }

    trackEvent("send.message", { message: message });
    setIsLoading(true);

    // Add the message to the conversation
    setConversation([
      ...conversation,
      { content: message, role: "user" },
      { content: null, role: "system" },
    ]);

    // Clear the message & remove empty chat
    setMessage("");
    setShowEmptyChat(false);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/whatsapp-chat-bot/ask-question`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            // messages: [...conversation, { content: message, role: "user" }],
            // model: selectedModel,
            question: message,
            number: encodedNumber,
          }),
        }
      );

      if (response.ok) {
        const data = await response.json();
        console.log("🚀 ~ file: Chat.tsx:158 ~ sendMessage ~ data:", data);

        console.log(
          "🚀 ~ file: Chat.tsx:170 ~ sendMessage ~ data?.history:",
          data?.data?.conversation
        );
        var chat_history_data = data?.data?.conversation?.messages;
        // Add the message to the conversation
        if (chat_history_data?.length > 0) {
          var last_message = chat_history_data.slice(-2);
          var messages_data = [...conversation];
          if (last_message) {
            for (var m = 0; m < last_message.length; m++) {
              messages_data.push(last_message[m]);
            }
          }
          setConversation(messages_data);
        }
      } else {
        console.error(response);
        setErrorMessage(response.statusText);
      }

      setIsLoading(false);
    } catch (error: any) {
      console.error(error);
      setErrorMessage(error.message);

      setIsLoading(false);
    }
  };
  const handleKeypress = (e: any) => {
    // It's triggers by pressing the enter key
    if (e.keyCode == 13 && !e.shiftKey) {
      sendMessage(e);
      e.preventDefault();
    }
  };

  return (
    <div className="flex max-w-full flex-1 flex-col">
      <div className="sticky top-0 z-10 flex items-center border-b border-white/20 bg-gray-800 pl-1 pt-1 text-gray-200 sm:pl-3 md:hidden">
        <button
          type="button"
          className="-ml-0.5 -mt-0.5 inline-flex h-10 w-10 items-center justify-center rounded-md hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white dark:hover:text-white"
          onClick={toggleComponentVisibility}
        >
          <span className="sr-only">Open sidebar</span>
          <RxHamburgerMenu className="h-6 w-6 text-white" />
        </button>
        <button type="button" className="px-3">
          <BsPlusLg className="h-6 w-6" />
        </button>
      </div>
      <div className="relative h-full w-full transition-width flex flex-col overflow-hidden items-stretch flex-1">
        <div className="flex-1 overflow-hidden">
          <div className="react-scroll-to-bottom--css-ikyem-79elbk h-full bg-[#FCFCF9] dark:bg-[#FCFCF9]">
            <div className="react-scroll-to-bottom--css-ikyem-1n7m0yu">
              {!showEmptyChat && conversation.length > 0 ? (
                <div className="flex flex-col items-center text-sm bg-[#FCFCF9]">
                  {conversation.map((message, index) => (
                    <Message key={index} message={message} />
                  ))}
                  <div className="w-full h-32 md:h-48 flex-shrink-0"></div>
                  <div ref={bottomOfChatRef}></div>
                </div>
              ) : null}
              {showEmptyChat ? (
                <div className="py-10 relative w-full flex flex-col h-full">
                  <h1 className="text-2xl sm:text-4xl font-semibold text-center text-[#13343B] dark:text-[#13343B] flex gap-2 items-center justify-center h-screen">
                    Klomena
                  </h1>
                </div>
              ) : null}
              <div className="flex flex-col items-center text-sm dark:bg-gray-800"></div>
            </div>
          </div>
        </div>
        <div className="absolute bottom-0 left-0 w-full border-t md:border-t-0 dark:border-white/20 md:border-transparent md:dark:border-transparent md:bg-vert-light-gradient bg-white dark:bg-gray-800 md:!bg-transparent dark:md:bg-vert-dark-gradient pt-2">
          <form className="stretch mx-2 flex flex-row gap-3 last:mb-2 md:mx-4 md:last:mb-6 lg:mx-auto lg:max-w-2xl xl:max-w-3xl">
            <div className="relative flex flex-col h-full flex-1 items-stretch md:flex-col">
              {errorMessage ? (
                <div className="mb-2 md:mb-0">
                  <div className="h-full flex ml-1 md:w-full md:m-auto md:mb-2 gap-0 md:gap-2 justify-center">
                    <span className="text-red-500 text-sm">{errorMessage}</span>
                  </div>
                </div>
              ) : null}
              <div className="flex flex-col w-full py-2 flex-grow md:py-3 mb-9 md:pl-4 relative border border-[#D3D3D3] bg-[#FCFCF9] dark:border-[#D3D3D3] dark:text-white dark:bg-[#FCFCF9] rounded-md shadow-[0_0_10px_rgba(0,0,0,0.10)] dark:shadow-[0_0_15px_rgba(0,0,0,0.10)]">
                <textarea
                  ref={textAreaRef}
                  value={message}
                  tabIndex={0}
                  data-id="root"
                  style={{
                    height: "24px",
                    maxHeight: "200px",
                    overflowY: "hidden",
                    color: "#000",
                  }}
                  // rows={1}
                  placeholder="Send a message..."
                  className="m-0 w-full resize-none border-0 bg-transparent p-0 pr-7 focus:ring-0 focus-visible:ring-0 dark:bg-transparent pl-2 md:pl-0"
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyDown={handleKeypress}
                ></textarea>
                <button
                  disabled={isLoading || message?.length === 0}
                  onClick={sendMessage}
                  className="absolute p-1 rounded-md bottom-1.5 md:bottom-3 bg-green-700 disabled:bg-gray-500 right-1 md:right-2 disabled:opacity-40 cursor:pointer"
                >
                  <FiSend className="h-4 w-4 mr-1 text-white " />
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Chat;
