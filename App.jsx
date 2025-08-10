import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ArrowRight, Stethoscope, Brain, Heart, Shield, Clock, Globe } from 'lucide-react';
import Header from './components/Header';
import SymptomAnalyzer from './components/SymptomAnalyzer';
import ImageAnalyzer from './components/ImageAnalyzer';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [language, setLanguage] = useState('en');

  const translations = {
    en: {
      title: 'Medical AI Assistant',
      subtitle: 'Intelligent Health Analysis',
      welcome: 'Welcome to Medical AI Assistant',
      description: 'Advanced AI-powered health analysis for symptoms and skin conditions',
      getStarted: 'Get Started',
      nextPage: 'Next Page',
      features: 'Features',
      symptomAnalysis: 'Symptom Analysis',
      symptomDesc: 'Describe your symptoms in natural language and get AI-powered insights',
      skinAnalysis: 'Skin Analysis',
      skinDesc: 'Upload images of skin conditions for detailed AI analysis',
      multilingualSupport: 'Multilingual Support',
      multilingualDesc: 'Full support for English and Arabic languages',
      securePrivate: 'Secure & Private',
      secureDesc: 'Your health data is protected with enterprise-grade security',
      highAccuracy: 'High Accuracy',
      accuracyDesc: 'Advanced AI models trained on medical datasets',
      instantResults: 'Instant Results',
      resultsDesc: 'Get analysis results in seconds, not hours',
      howItWorks: 'How It Works',
      step1: 'Describe Symptoms',
      step1Desc: 'Tell us about your symptoms in your own words',
      step2: 'AI Analysis',
      step2Desc: 'Our AI analyzes your input using medical knowledge',
      step3: 'Get Insights',
      step3Desc: 'Receive detailed analysis and recommendations',
      disclaimer: 'Important Notice',
      disclaimerText: 'This tool is for informational purposes only and does not replace professional medical advice. Always consult with healthcare professionals for medical concerns.',
      chooseAnalysis: 'Choose Analysis Type',
      chooseDesc: 'Select the type of medical analysis you need',
      analyzeSymptoms: 'Analyze Symptoms',
      analyzeSkin: 'Analyze Skin Condition'
    },
    ar: {
      title: 'مساعد الذكاء الاصطناعي الطبي',
      subtitle: 'تحليل صحي ذكي',
      welcome: 'مرحباً بك في مساعد الذكاء الاصطناعي الطبي',
      description: 'تحليل صحي متقدم مدعوم بالذكاء الاصطناعي للأعراض والحالات الجلدية',
      getStarted: 'ابدأ الآن',
      nextPage: 'الصفحة التالية',
      features: 'المميزات',
      symptomAnalysis: 'تحليل الأعراض',
      symptomDesc: 'اوصف أعراضك بلغة طبيعية واحصل على رؤى مدعومة بالذكاء الاصطناعي',
      skinAnalysis: 'تحليل الجلد',
      skinDesc: 'ارفع صور الحالات الجلدية للحصول على تحليل مفصل بالذكاء الاصطناعي',
      multilingualSupport: 'دعم متعدد اللغات',
      multilingualDesc: 'دعم كامل للغتين الإنجليزية والعربية',
      securePrivate: 'آمن وخاص',
      secureDesc: 'بياناتك الصحية محمية بأمان على مستوى المؤسسات',
      highAccuracy: 'دقة عالية',
      accuracyDesc: 'نماذج ذكاء اصطناعي متقدمة مدربة على مجموعات بيانات طبية',
      instantResults: 'نتائج فورية',
      resultsDesc: 'احصل على نتائج التحليل في ثوانٍ وليس ساعات',
      howItWorks: 'كيف يعمل',
      step1: 'اوصف الأعراض',
      step1Desc: 'أخبرنا عن أعراضك بكلماتك الخاصة',
      step2: 'تحليل الذكاء الاصطناعي',
      step2Desc: 'يحلل الذكاء الاصطناعي مدخلاتك باستخدام المعرفة الطبية',
      step3: 'احصل على الرؤى',
      step3Desc: 'تلقى تحليلاً مفصلاً وتوصيات',
      disclaimer: 'إشعار مهم',
      disclaimerText: 'هذه الأداة لأغراض إعلامية فقط ولا تحل محل المشورة الطبية المهنية. استشر دائماً أخصائيي الرعاية الصحية للمخاوف الطبية.',
      chooseAnalysis: 'اختر نوع التحليل',
      chooseDesc: 'اختر نوع التحليل الطبي الذي تحتاجه',
      analyzeSymptoms: 'تحليل الأعراض',
      analyzeSkin: 'تحليل الحالة الجلدية'
    }
  };

  const t = translations[language];

  const HomePage = () => (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
      <div className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="flex justify-center items-center mb-6">
            <div className="bg-blue-600 p-4 rounded-full">
              <Stethoscope className="h-12 w-12 text-white" />
            </div>
          </div>
          <h1 className="text-5xl font-bold text-gray-900 mb-4">{t.welcome}</h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">{t.description}</p>
          <Button 
            onClick={() => setCurrentPage('choose')}
            size="lg" 
            className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 text-lg rounded-full shadow-lg hover:shadow-xl transition-all duration-300"
          >
            {t.getStarted}
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
        </div>

        {/* Features Grid */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">{t.features}</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="hover:shadow-lg transition-shadow duration-300 border-0 shadow-md">
              <CardHeader className="text-center">
                <div className="bg-blue-100 p-3 rounded-full w-fit mx-auto mb-4">
                  <Brain className="h-8 w-8 text-blue-600" />
                </div>
                <CardTitle className="text-xl">{t.symptomAnalysis}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-center text-gray-600">
                  {t.symptomDesc}
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-shadow duration-300 border-0 shadow-md">
              <CardHeader className="text-center">
                <div className="bg-green-100 p-3 rounded-full w-fit mx-auto mb-4">
                  <Heart className="h-8 w-8 text-green-600" />
                </div>
                <CardTitle className="text-xl">{t.skinAnalysis}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-center text-gray-600">
                  {t.skinDesc}
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-shadow duration-300 border-0 shadow-md">
              <CardHeader className="text-center">
                <div className="bg-purple-100 p-3 rounded-full w-fit mx-auto mb-4">
                  <Globe className="h-8 w-8 text-purple-600" />
                </div>
                <CardTitle className="text-xl">{t.multilingualSupport}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-center text-gray-600">
                  {t.multilingualDesc}
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-shadow duration-300 border-0 shadow-md">
              <CardHeader className="text-center">
                <div className="bg-orange-100 p-3 rounded-full w-fit mx-auto mb-4">
                  <Shield className="h-8 w-8 text-orange-600" />
                </div>
                <CardTitle className="text-xl">{t.securePrivate}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-center text-gray-600">
                  {t.secureDesc}
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-shadow duration-300 border-0 shadow-md">
              <CardHeader className="text-center">
                <div className="bg-red-100 p-3 rounded-full w-fit mx-auto mb-4">
                  <Stethoscope className="h-8 w-8 text-red-600" />
                </div>
                <CardTitle className="text-xl">{t.highAccuracy}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-center text-gray-600">
                  {t.accuracyDesc}
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-shadow duration-300 border-0 shadow-md">
              <CardHeader className="text-center">
                <div className="bg-teal-100 p-3 rounded-full w-fit mx-auto mb-4">
                  <Clock className="h-8 w-8 text-teal-600" />
                </div>
                <CardTitle className="text-xl">{t.instantResults}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-center text-gray-600">
                  {t.resultsDesc}
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* How It Works */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">{t.howItWorks}</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-blue-600 text-white rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="text-xl font-semibold mb-2">{t.step1}</h3>
              <p className="text-gray-600">{t.step1Desc}</p>
            </div>
            <div className="text-center">
              <div className="bg-green-600 text-white rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="text-xl font-semibold mb-2">{t.step2}</h3>
              <p className="text-gray-600">{t.step2Desc}</p>
            </div>
            <div className="text-center">
              <div className="bg-purple-600 text-white rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="text-xl font-semibold mb-2">{t.step3}</h3>
              <p className="text-gray-600">{t.step3Desc}</p>
            </div>
          </div>
        </div>

        {/* Next Page Button */}
        <div className="text-center mb-16">
          <Button 
            onClick={() => setCurrentPage('choose')}
            size="lg" 
            className="bg-gradient-to-r from-blue-600 to-green-600 hover:from-blue-700 hover:to-green-700 text-white px-12 py-4 text-lg rounded-full shadow-lg hover:shadow-xl transition-all duration-300"
          >
            {t.nextPage}
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
        </div>

        {/* Disclaimer */}
        <Card className="bg-yellow-50 border-yellow-200">
          <CardHeader>
            <CardTitle className="text-yellow-800 flex items-center">
              <Shield className="mr-2 h-5 w-5" />
              {t.disclaimer}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-yellow-700">{t.disclaimerText}</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );

  const ChoosePage = () => (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">{t.chooseAnalysis}</h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">{t.chooseDesc}</p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {/* Symptom Analysis Card */}
          <Card 
            className="hover:shadow-2xl transition-all duration-300 cursor-pointer border-0 shadow-lg hover:scale-105"
            onClick={() => setCurrentPage('symptoms')}
          >
            <CardHeader className="text-center pb-6">
              <div className="bg-gradient-to-br from-blue-500 to-blue-600 p-6 rounded-full w-fit mx-auto mb-6">
                <Brain className="h-16 w-16 text-white" />
              </div>
              <CardTitle className="text-2xl text-gray-900">{t.analyzeSymptoms}</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <CardDescription className="text-gray-600 text-lg mb-6">
                {t.symptomDesc}
              </CardDescription>
              <Button 
                className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-full"
                onClick={() => setCurrentPage('symptoms')}
              >
                {t.analyzeSymptoms}
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </CardContent>
          </Card>

          {/* Skin Analysis Card */}
          <Card 
            className="hover:shadow-2xl transition-all duration-300 cursor-pointer border-0 shadow-lg hover:scale-105"
            onClick={() => setCurrentPage('skin')}
          >
            <CardHeader className="text-center pb-6">
              <div className="bg-gradient-to-br from-green-500 to-green-600 p-6 rounded-full w-fit mx-auto mb-6">
                <Heart className="h-16 w-16 text-white" />
              </div>
              <CardTitle className="text-2xl text-gray-900">{t.analyzeSkin}</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <CardDescription className="text-gray-600 text-lg mb-6">
                {t.skinDesc}
              </CardDescription>
              <Button 
                className="bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-full"
                onClick={() => setCurrentPage('skin')}
              >
                {t.analyzeSkin}
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Back Button */}
        <div className="text-center mt-12">
          <Button 
            variant="outline" 
            onClick={() => setCurrentPage('home')}
            className="px-8 py-3 rounded-full"
          >
            ← {language === 'en' ? 'Back to Home' : 'العودة للرئيسية'}
          </Button>
        </div>
      </div>
    </div>
  );

  return (
    <div className={`min-h-screen ${language === 'ar' ? 'rtl' : 'ltr'}`}>
      <Header language={language} setLanguage={setLanguage} />
      
      {currentPage === 'home' && <HomePage />}
      {currentPage === 'choose' && <ChoosePage />}
      {currentPage === 'symptoms' && (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
          <div className="container mx-auto px-4 py-8">
            <Button 
              variant="outline" 
              onClick={() => setCurrentPage('choose')}
              className="mb-6 px-6 py-2 rounded-full"
            >
              ← {language === 'en' ? 'Back' : 'رجوع'}
            </Button>
            <SymptomAnalyzer language={language} />
          </div>
        </div>
      )}
      {currentPage === 'skin' && (
        <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-blue-50">
          <div className="container mx-auto px-4 py-8">
            <Button 
              variant="outline" 
              onClick={() => setCurrentPage('choose')}
              className="mb-6 px-6 py-2 rounded-full"
            >
              ← {language === 'en' ? 'Back' : 'رجوع'}
            </Button>
            <ImageAnalyzer language={language} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

