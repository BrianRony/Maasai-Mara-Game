import React from 'react';
import { useRouteError, Link } from "react-router-dom";

function ErrorPage() {
  const error = useRouteError();
  console.error(error);

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-4 text-center">
      <div className="bg-gray-800 border-2 border-red-600 rounded-xl p-8 shadow-2xl max-w-md w-full">
        <h1 className="text-4xl font-bold text-red-500 mb-4">Oops!</h1>
        <p className="text-gray-300 mb-6">Something went wrong in the wild.</p>
        <p className="text-gray-500 italic mb-8">
          {error.statusText || error.message}
        </p>
        <Link 
          to="/" 
          className="bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-6 rounded-lg transition"
        >
          Return to Base Camp
        </Link>
      </div>
    </div>
  );
}

export default ErrorPage;
