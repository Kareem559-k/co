import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Globe, Menu, X, Stethoscope } from 'lucide-react'
import '../App.css'

const Header = ({ language, setLanguage, isMenuOpen, setIsMenuOpen }) => {
  const toggleLanguage = () => {
    setLanguage(language === 'en' ? 'ar' : 'en')
  }

  const text = {
    en: {
      title: 'Medical AI Assistant',
      subtitle: 'Intelligent Health Analysis',
      menu: 'Menu',
      language: 'العربية'
    },
    ar: {
      title: 'مساعد الذكاء الاصطناعي الطبي',
      subtitle: 'تحليل صحي ذكي',
      menu: 'القائمة',
      language: 'English'
    }
  }

  return (
    <header className="bg-white shadow-lg border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Title */}
          <div className={`flex items-center space-x-3 ${language === 'ar' ? 'flex-row-reverse space-x-reverse' : ''}`}>
            <div className="flex items-center justify-center w-10 h-10 bg-blue-600 rounded-lg">
              <Stethoscope className="w-6 h-6 text-white" />
            </div>
            <div className={`${language === 'ar' ? 'text-right' : 'text-left'}`}>
              <h1 className="text-xl font-bold text-gray-900">
                {text[language].title}
              </h1>
              <p className="text-sm text-gray-600">
                {text[language].subtitle}
              </p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-4">
            <Button
              variant="outline"
              size="sm"
              onClick={toggleLanguage}
              className="flex items-center space-x-2"
            >
              <Globe className="w-4 h-4" />
              <span>{text[language].language}</span>
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="p-2"
            >
              {isMenuOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </Button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-200">
            <div className="flex flex-col space-y-3">
              <Button
                variant="outline"
                size="sm"
                onClick={toggleLanguage}
                className="flex items-center justify-center space-x-2 w-full"
              >
                <Globe className="w-4 h-4" />
                <span>{text[language].language}</span>
              </Button>
            </div>
          </div>
        )}
      </div>
    </header>
  )
}

export default Header

