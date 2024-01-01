import { useEffect, useState } from "react";
import Chat from "@/components/Chat";
import MobileSiderbar from "@/components/MobileSidebar";
import Sidebar from "@/components/Sidebar";
import useAnalytics from "@/hooks/useAnalytics";
import { useRouter } from "next/router";

export default function Home() {
  const [isComponentVisible, setIsComponentVisible] = useState(false);
  const { trackEvent } = useAnalytics();

  const router = useRouter();

  useEffect(() => {
    trackEvent("page.view", { page: "home" });
  }, []);

  const toggleComponentVisibility = () => {
    setIsComponentVisible(!isComponentVisible);
  };

  return (
    <main className="overflow-hidden w-full h-screen relative flex">
      {isComponentVisible ? (
        <MobileSiderbar toggleComponentVisibility={toggleComponentVisibility} />
      ) : null}
      <div className="dark hidden flex-shrink-0 bg-[#f3f2ee] md:flex md:w-[230px] md:flex-col">
        <div className="flex h-full min-h-0 flex-col ">
          <Sidebar />
        </div>
      </div>
      <Chat
        toggleComponentVisibility={toggleComponentVisibility}
        encodedNumber={router?.query?.number}
      />
    </main>
  );
}
