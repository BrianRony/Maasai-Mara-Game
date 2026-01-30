import React from 'react';

const SafariLayout = ({ children, title, subtitle }) => {
  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-4 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')]">
      {/* Main Game Card */}
      <div className="w-full max-w-2xl bg-gray-800 border-2 border-yellow-600 rounded-xl shadow-2xl overflow-hidden relative">
        
        {/* Decorative Top Bar */}
        <div className="h-2 bg-gradient-to-r from-yellow-600 via-yellow-400 to-yellow-600"></div>

        <div className="p-8 text-center">
          {/* Header Section */}
          {(title || subtitle) && (
            <div className="mb-8 border-b border-gray-700 pb-4">
              {title && <h1 className="text-4xl font-bold text-yellow-500 tracking-wide uppercase drop-shadow-md">{title}</h1>}
              {subtitle && <p className="text-gray-400 text-lg mt-2 italic">{subtitle}</p>}
            </div>
          )}

          {/* Dynamic Content */}
          <div className="text-gray-200">
            {children}
          </div>
        </div>

        {/* Decorative Bottom Bar */}
        <div className="h-2 bg-gradient-to-r from-yellow-600 via-yellow-400 to-yellow-600 mt-auto"></div>
      </div>
      
      {/* Footer / Copyright */}
      <div className="mt-8 text-gray-500 text-xs">
        © 2026 Maasai Mara Adventures
      </div>
    </div>
  );
};

export default SafariLayout;
