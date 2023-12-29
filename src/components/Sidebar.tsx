import React from "react";
import {
  AiOutlineMessage,
  AiOutlinePlus,
  AiOutlineUser,
  AiOutlineSetting,
} from "react-icons/ai";
import { BiLinkExternal } from "react-icons/bi";
import { FiMessageSquare } from "react-icons/fi";
import { MdLogout } from "react-icons/md";

const Sidebar = () => {
  return (
    <div className="scrollbar-trigger flex h-full w-full flex-1 items-start border-white/20">
      <nav className="flex h-full flex-1 flex-col space-y-1 p-2">
        <div className="flex-col flex-1 overflow-y-auto border-b border-white/20">
          <div className="flex flex-col gap-2 pb-2 text-gray-100 text-sm">
            <a className="flex py-3 px-3 items-center gap-3 relative rounded-md cursor-pointer break-all hover:pr-4 group">
              <div className="flex-1 text-ellipsis max-h-5 overflow-hidden break-all relative text-[#13343B] font-bold text-[19px]">
                Klomena
              </div>
            </a>
            <a className="flex py-3 px-3 items-center gap-3 relative rounded-md bg-[#f3f2ee] cursor-pointer break-all hover:pr-4 group">
              <FiMessageSquare className="h-4 w-4 text-[#13343B]" />
              <div className="flex-1 text-ellipsis max-h-5 overflow-hidden break-all relative text-[#13343B] font-semibold">
                Discovery
              </div>
            </a>
          </div>
        </div>
      </nav>
    </div>
  );
};

export default Sidebar;
