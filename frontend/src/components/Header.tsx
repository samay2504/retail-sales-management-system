/**
 * Header component
 */

export const Header = () => {
  return (
    <header className="glass-card mb-8 sticky top-0 z-50">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-10 h-10 bg-gradient-cta rounded-full flex items-center justify-center">
              <span className="text-white font-bold text-xl">T</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-cyan bg-clip-text text-transparent">
                TruEstate
              </h1>
              <p className="text-xs text-gray-400">Retail Sales Management</p>
            </div>
          </div>
          
          <nav className="hidden md:flex items-center space-x-6">
            <a href="#" className="text-gray-300 hover:text-primary transition-colors">
              Dashboard
            </a>
            <a href="#" className="text-gray-300 hover:text-primary transition-colors">
              Analytics
            </a>
            <a href="#" className="text-gray-300 hover:text-primary transition-colors">
              Reports
            </a>
          </nav>
          
          <div className="flex items-center space-x-4">
            <button className="btn-secondary text-sm py-2 px-4">
              Sign In
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};
