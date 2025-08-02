import { useState, useEffect, useCallback, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Play, Pause, RotateCcw, SkipForward, Gamepad2, Smartphone, Sparkles } from "lucide-react";

interface Scene {
  message: string;
  scene: 'hamburger' | 'hotdog' | 'pizza' | 'all-foods';
  duration: number;
}

const scenes: Scene[] = [
  { message: "Let's make a delicious hamburger!", scene: 'hamburger', duration: 2000 },
  { message: "Grilling the patty and assembling the bun...", scene: 'hamburger', duration: 2000 },
  { message: "Now for a classic hotdog!", scene: 'hotdog', duration: 2000 },
  { message: "Sizzling sausage with a mustard drizzle!", scene: 'hotdog', duration: 2000 },
  { message: "Time for a cheesy pizza!", scene: 'pizza', duration: 2000 },
  { message: "Baking the crust with toppings galore!", scene: 'pizza', duration: 2000 },
  { message: "All done! Which is your favorite?", scene: 'all-foods', duration: 3000 }
];

export default function Home() {
  const [currentSceneIndex, setCurrentSceneIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const clearTimer = useCallback(() => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  const stopAnimation = useCallback(() => {
    clearTimer();
    setIsPlaying(false);
    setIsPaused(false);
  }, [clearTimer]);

  const nextScene = useCallback(() => {
    setCurrentSceneIndex(prev => {
      const next = prev + 1;
      if (next >= scenes.length) {
        setIsPlaying(false);
        setIsPaused(false);
        return prev;
      }
      return next;
    });
  }, []);

  const startTimer = useCallback((duration: number) => {
    clearTimer();
    timerRef.current = setTimeout(nextScene, duration);
  }, [clearTimer, nextScene]);

  const playAnimation = useCallback(() => {
    if (currentSceneIndex >= scenes.length) {
      stopAnimation();
      return;
    }

    setIsPlaying(true);
    setIsPaused(false);
    startTimer(scenes[currentSceneIndex].duration);
  }, [currentSceneIndex, stopAnimation, startTimer]);

  const pauseAnimation = useCallback(() => {
    clearTimer();
    setIsPlaying(false);
    setIsPaused(true);
  }, [clearTimer]);

  const restartAnimation = useCallback(() => {
    clearTimer();
    setIsPlaying(false);
    setIsPaused(false);
    setCurrentSceneIndex(0);
  }, [clearTimer]);

  const skipScene = useCallback(() => {
    if (isPlaying && currentSceneIndex < scenes.length - 1) {
      clearTimer();
      nextScene();
    }
  }, [isPlaying, currentSceneIndex, clearTimer, nextScene]);

  const handlePlay = useCallback(() => {
    if (isPaused) {
      // Resume from current position
      setIsPaused(false);
      setIsPlaying(true);
      startTimer(scenes[currentSceneIndex].duration);
    } else if (currentSceneIndex >= scenes.length) {
      // Restart from beginning when animation is complete
      setCurrentSceneIndex(0);
      setIsPlaying(true);
      setIsPaused(false);
      setTimeout(() => {
        startTimer(scenes[0].duration);
      }, 100);
    } else {
      // Start from beginning
      setCurrentSceneIndex(0);
      setIsPlaying(true);
      setIsPaused(false);
      setTimeout(() => {
        startTimer(scenes[0].duration);
      }, 100);
    }
  }, [isPaused, currentSceneIndex, startTimer]);

  // Continue animation when scene changes during play
  useEffect(() => {
    if (isPlaying && !isPaused && currentSceneIndex < scenes.length) {
      startTimer(scenes[currentSceneIndex].duration);
    }
  }, [currentSceneIndex, isPlaying, isPaused, startTimer]);

  // Cleanup on unmount
  useEffect(() => {
    return () => clearTimer();
  }, [clearTimer]);

  // Keyboard controls
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      switch(e.code) {
        case 'Space':
          e.preventDefault();
          if (isPlaying) {
            pauseAnimation();
          } else {
            handlePlay();
          }
          break;
        case 'KeyR':
          e.preventDefault();
          restartAnimation();
          break;
        case 'ArrowRight':
          e.preventDefault();
          skipScene();
          break;
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isPlaying, handlePlay, pauseAnimation, restartAnimation, skipScene]);

  const currentScene = scenes[currentSceneIndex] || { message: "Ready to start the show?", scene: 'hamburger', duration: 0 };
  const progressPercent = currentSceneIndex >= scenes.length ? 100 : ((currentSceneIndex + 1) / scenes.length) * 100;

  const renderScene = () => {
    if (currentSceneIndex >= scenes.length) {
      return (
        <div className="text-center">
          <div className="flex justify-center space-x-4 mb-4">
            <span className="text-4xl">🍔</span>
            <span className="text-4xl">🌭</span>
            <span className="text-4xl">🍕</span>
          </div>
          <div className="ascii-art text-[hsl(var(--food-mint))] font-bold text-lg mb-4">
            {`╔═══════════════════╗
║  🍔    🌭    🍕  ║
║  The Perfect Trio ║
╚═══════════════════╝`}
          </div>
          <p className="text-gray-700 max-w-md mx-auto text-lg">
            <strong>Animation completed!</strong><br />
            <span className="text-sm text-gray-500 mt-2 block">Click restart to watch again!</span>
          </p>
        </div>
      );
    }

    if (!isPlaying && !isPaused && currentSceneIndex === 0) {
      return (
        <div className="text-center">
          <div className="text-6xl mb-4">🎬</div>
          <p className="text-gray-500 text-lg">Ready to start the show?</p>
          <p className="text-gray-400 text-sm mt-2">Click play to begin the delicious animation!</p>
        </div>
      );
    }

    switch (currentScene.scene) {
      case 'hamburger':
        return (
          <div className="text-center scene-transition">
            <div className="food-emoji mb-4">🍔</div>
            <div className="ascii-art text-[hsl(var(--food-orange))] font-bold text-lg mb-4">
              {`┌─────────────┐
│   /‾‾‾‾‾\\   │
│  │ 🍔 │  │
│   \\____/   │
└─────────────┘`}
            </div>
            <p className="text-gray-700 max-w-md mx-auto">
              <strong>Hamburger:</strong> Juicy beef patty, fresh lettuce, tomato, and a toasted bun! The classic American favorite.
            </p>
          </div>
        );
      case 'hotdog':
        return (
          <div className="text-center scene-transition">
            <div className="food-emoji mb-4">🌭</div>
            <div className="ascii-art text-[hsl(var(--food-yellow))] font-bold text-lg mb-4">
              {`┌─────────────┐
│ ═══🌭═══ │
│  \\______/  │
│   Mustard   │
└─────────────┘`}
            </div>
            <p className="text-gray-700 max-w-md mx-auto">
              <strong>Hotdog:</strong> Grilled sausage nestled in a soft bun with a perfect drizzle of mustard!
            </p>
          </div>
        );
      case 'pizza':
        return (
          <div className="text-center scene-transition">
            <div className="food-emoji mb-4">🍕</div>
            <div className="ascii-art text-[hsl(var(--food-green))] font-bold text-lg mb-4">
              {`┌─────────────┐
│   /‾‾‾‾‾\\   │
│  │ 🍕 │  │
│   \\____/   │
└─────────────┘`}
            </div>
            <p className="text-gray-700 max-w-md mx-auto">
              <strong>Pizza:</strong> Cheesy, tomato-sauced delight with a perfectly crispy crust and fresh toppings!
            </p>
          </div>
        );
      case 'all-foods':
        return (
          <div className="text-center scene-transition">
            <div className="flex justify-center space-x-4 mb-4">
              <span className="text-4xl">🍔</span>
              <span className="text-4xl">🌭</span>
              <span className="text-4xl">🍕</span>
            </div>
            <div className="ascii-art text-[hsl(var(--food-mint))] font-bold text-lg mb-4">
              {`╔═══════════════════╗
║  🍔    🌭    🍕  ║
║  The Perfect Trio ║
╚═══════════════════╝`}
            </div>
            <p className="text-gray-700 max-w-md mx-auto text-lg">
              <strong>All done! Which is your favorite?</strong><br />
              <span className="text-sm text-gray-500 mt-2 block">The ultimate food experience in ASCII art!</span>
            </p>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="bg-gradient-to-br from-slate-50 to-slate-100 min-h-screen">
      {/* Header */}
      <header className="text-center py-8 animate-slide-up">
        <h1 className="text-4xl md:text-5xl font-bold text-[hsl(var(--dark-slate))] mb-2">
          <span className="text-[hsl(var(--food-orange))]">🍔</span> Food Animation Show <span className="text-[hsl(var(--food-yellow))]">🍕</span>
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto px-4">
          Watch delicious ASCII art come to life! Experience the magic of hamburgers, hotdogs, and pizza in an interactive animated sequence.
        </p>
      </header>

      {/* Main Animation Container */}
      <main className="container mx-auto px-4 max-w-4xl">
        <Card className="rounded-2xl shadow-xl mb-8 animate-fade-in">
          <CardContent className="p-8">
            {/* Animation Display */}
            <div className="text-center mb-8">
              <div className="text-2xl font-semibold text-[hsl(var(--dark-slate))] mb-6 min-h-[2rem] scene-transition">
                {currentSceneIndex >= scenes.length ? "Animation completed! Click restart to watch again." : currentScene.message}
              </div>
              
              {/* Animation Display Area */}
              <div className="bg-gray-50 rounded-xl p-8 min-h-[400px] flex flex-col items-center justify-center border-2 border-dashed border-gray-200">
                {renderScene()}
              </div>
            </div>

            {/* Progress Indicator */}
            <div className="mb-6">
              <div className="flex justify-between text-sm text-gray-500 mb-2">
                <span>Scene {Math.min(currentSceneIndex + 1, scenes.length)} of {scenes.length}</span>
                <span>Duration: {currentScene.duration / 1000}s</span>
              </div>
              
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div 
                  className="bg-gradient-to-r from-[hsl(var(--food-orange))] to-[hsl(var(--food-yellow))] h-3 rounded-full progress-bar" 
                  style={{ width: `${progressPercent}%` }}
                />
              </div>
              
              <div className="flex justify-between mt-2 text-xs text-gray-400">
                <span>🍔 Hamburger</span>
                <span>🌭 Hotdog</span>
                <span>🍕 Pizza</span>
                <span>🎉 Finale</span>
              </div>
            </div>

            {/* Control Panel */}
            <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-4">
              {!isPlaying || isPaused || currentSceneIndex >= scenes.length ? (
                <Button 
                  onClick={handlePlay}
                  className="control-button bg-[hsl(var(--food-orange))] hover:bg-[hsl(14,100%,55%)] text-white px-8 py-3 rounded-full font-semibold shadow-lg"
                >
                  <Play className="w-4 h-4 mr-2" />
                  {currentSceneIndex >= scenes.length ? "Play Again" : isPaused ? "Resume" : "Play"}
                </Button>
              ) : (
                <Button 
                  onClick={pauseAnimation}
                  className="control-button bg-gray-500 hover:bg-gray-600 text-white px-8 py-3 rounded-full font-semibold shadow-lg"
                >
                  <Pause className="w-4 h-4 mr-2" />
                  Pause
                </Button>
              )}
              
              <Button 
                onClick={restartAnimation}
                className="control-button bg-[hsl(var(--food-yellow))] hover:bg-[hsl(46,100%,55%)] text-[hsl(var(--dark-slate))] px-8 py-3 rounded-full font-semibold shadow-lg"
              >
                <RotateCcw className="w-4 h-4 mr-2" />
                Restart
              </Button>
              
              <Button 
                onClick={skipScene}
                className="control-button bg-[hsl(var(--food-mint))] hover:bg-[hsl(178,60%,50%)] text-white px-6 py-3 rounded-full font-semibold shadow-lg"
              >
                <SkipForward className="w-4 h-4 mr-2" />
                Skip
              </Button>
            </div>
          </CardContent>
        </Card>
        
        {/* Feature Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Card className="shadow-lg animate-fade-in">
            <CardContent className="p-6 text-center">
              <div className="text-3xl mb-3"><Gamepad2 className="w-8 h-8 mx-auto" /></div>
              <h3 className="font-semibold text-[hsl(var(--dark-slate))] mb-2">Interactive Controls</h3>
              <p className="text-gray-600 text-sm">Play, pause, restart, and skip through scenes with intuitive media controls.</p>
            </CardContent>
          </Card>
          
          <Card className="shadow-lg animate-fade-in">
            <CardContent className="p-6 text-center">
              <div className="text-3xl mb-3"><Smartphone className="w-8 h-8 mx-auto" /></div>
              <h3 className="font-semibold text-[hsl(var(--dark-slate))] mb-2">Mobile Responsive</h3>
              <p className="text-gray-600 text-sm">Enjoy the experience on any device with our fully responsive design.</p>
            </CardContent>
          </Card>
          
          <Card className="shadow-lg animate-fade-in">
            <CardContent className="p-6 text-center">
              <div className="text-3xl mb-3"><Sparkles className="w-8 h-8 mx-auto" /></div>
              <h3 className="font-semibold text-[hsl(var(--dark-slate))] mb-2">Smooth Animations</h3>
              <p className="text-gray-600 text-sm">Beautiful transitions and timing create an engaging viewing experience.</p>
            </CardContent>
          </Card>
        </div>
      </main>
      
      {/* Footer */}
      <footer className="text-center py-8 text-gray-500">
        <p>&copy; 2024 Made with ❤️ and lots of ASCII art!</p>
        <p className="text-sm mt-2">Try running the animation again for maximum enjoyment!</p>
      </footer>
    </div>
  );
}
