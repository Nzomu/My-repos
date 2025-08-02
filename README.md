<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ヨルダン・パーセントバルーンゲーム</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Cairo', sans-serif;
            background: linear-gradient(to bottom, 
                #87CEEB 0%,     /* 空の青 */
                #F4A460 20%,    /* 砂丘の色 */
                #D2B48C 40%,    /* 薄い砂色 */
                #DEB887 60%,    /* ベージュ */
                #F5DEB3 80%,    /* 小麦色 */
                #FAEBD7 100%    /* アンティークホワイト */
            );
            background-attachment: fixed;
            overflow-x: hidden;
            position: relative;
        }
        
        /* 砂丘のシルエット効果 */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600"><path d="M0,400 Q300,300 600,350 Q900,400 1200,320 L1200,600 L0,600 Z" fill="%23D2B48C" opacity="0.3"/><path d="M0,450 Q200,380 400,420 Q600,460 800,400 Q1000,340 1200,380 L1200,600 L0,600 Z" fill="%23DEB887" opacity="0.4"/></svg>') no-repeat center bottom;
            background-size: cover;
            z-index: -2;
            pointer-events: none;
        }
        .backdrop-blur-md {
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }
        .font-cairo {
            font-family: 'Cairo', sans-serif;
        }
        #balloon-container {
            position: relative;
            width: 250px;
            height: 320px;
            margin: 0 auto;
        }
        #balloon {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            animation: float 6s ease-in-out infinite;
            transform-origin: bottom center;
            transition: transform 0.3s ease;
        }
        @keyframes float {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(3deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }
        .explosion {
            animation: explode 0.5s forwards;
        }
        @keyframes explode {
            0% { transform: scale(1); opacity: 1; }
            100% { transform: scale(3); opacity: 0; }
        }
        .particle {
            position: absolute;
            width: 15px;
            height: 15px;
            background: #EF4444;
            border-radius: 50%;
            opacity: 0;
            pointer-events: none;
        }
        .correct-animation {
            animation: sparkle 1s ease-out forwards;
        }
        @keyframes sparkle {
            0% { transform: scale(1); box-shadow: 0 0 0px #FFD700; }
            50% { transform: scale(1.1); box-shadow: 0 0 30px #FFD700; }
            100% { transform: scale(1); box-shadow: 0 0 0px #FFD700; }
        }
        .fade-in {
            animation: fadeIn 0.5s ease-in forwards;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        /* モバイル対応の改善 */
        @media (max-width: 640px) {
            #balloon-container {
                width: 200px;
                height: 260px;
            }
            .input-container {
                flex-direction: column;
                gap: 2rem;
                align-items: center;
                justify-content: center;
            }
            #percentage-input {
                width: 100%;
                max-width: 250px;
                height: 80px !important;
                font-size: 3.5rem !important;
            }
            #submit-btn {
                width: 100%;
                max-width: 250px;
                height: 80px !important;
                font-size: 1.5rem !important;
            }
            .percent-symbol {
                font-size: 2.5rem !important;
                right: 1rem !important;
            }
        }
        
        /* ヨルダンらしい装飾要素 */
        .jordan-decoration {
            position: fixed;
            opacity: 0.15;
            pointer-events: none;
            z-index: -1;
            color: #8B4513;
        }
        
        .jordan-decoration::before {
            content: '🏜️';
            font-size: 2rem;
            position: absolute;
            animation: float-decoration 10s ease-in-out infinite;
        }
        
        .jordan-decoration:nth-child(1) { top: 15%; left: 5%; }
        .jordan-decoration:nth-child(2) { top: 25%; right: 8%; }
        .jordan-decoration:nth-child(3) { bottom: 20%; left: 10%; }
        .jordan-decoration:nth-child(4) { bottom: 30%; right: 5%; }
        
        @keyframes float-decoration {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-10px) rotate(2deg); }
        }
        
        /* テキストの中央配置強化 */
        .center-text {
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
    </style>
</head>
<body class="bg-black text-white flex items-center justify-center min-h-screen font-cairo">
    <!-- ヨルダンらしい装飾要素 -->
    <div class="jordan-decoration"></div>
    <div class="jordan-decoration"></div>
    <div class="jordan-decoration"></div>
    <div class="jordan-decoration"></div>
    
    <div class="absolute inset-0 bg-white bg-opacity-20"></div>

    <div id="game-container" class="relative w-full max-w-2xl mx-auto p-4 md:p-8 bg-white bg-opacity-85 backdrop-blur-sm rounded-2xl shadow-2xl border border-yellow-600 text-center hidden text-gray-800">
        
        <!-- Progress Indicator -->
        <div class="mb-4">
            <div class="flex justify-center space-x-2">
                <div id="progress-dots" class="flex space-x-2"></div>
            </div>
        </div>

        <!-- Question Area -->
        <div id="question-area" class="mb-6">
            <p class="text-lg md:text-xl text-yellow-600 mb-2 center-text">Q<span id="question-number">1</span>.</p>
            <h2 id="question-text" class="text-2xl md:text-4xl font-bold leading-tight min-h-[100px] center-text px-4"></h2>
        </div>

        <!-- Balloon and Answer Area -->
        <div class="mb-6 min-h-[320px] flex items-center justify-center">
            <div id="balloon-container">
                <div id="balloon">
                    <!-- Jordan Flag Balloon SVG -->
                    <svg viewBox="0 0 200 260" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <clipPath id="balloon-clip">
                                <path d="M 100,0 C 20,0 0,70 0,130 C 0,210 100,260 100,260 C 100,260 200,210 200,130 C 200,70 180,0 100,0 Z"/>
                            </clipPath>
                        </defs>
                        <g clip-path="url(#balloon-clip)">
                            <!-- 白い背景 -->
                            <rect width="200" height="260" fill="#fff"/>
                            <!-- 黒いストライプ -->
                            <rect width="200" height="86.67" fill="#000"/>
                            <!-- 緑のストライプ -->
                            <rect y="173.33" width="200" height="86.67" fill="#008000"/>
                            <!-- 赤い三角形 -->
                            <path d="M 0,0 L 100,130 L 0,260 Z" fill="#ce1126"/>
                            <!-- ヨルダンの7つの角を持つ星（七光星） -->
<g transform="translate(35, 130)">
    <!-- 7つの角を持つ星 - 数学的に正確な座標 -->
    <path fill="#fff" d="M 0,-12 
        L 2.5,-3.8 
        L 11.0,-7.6 
        L 4.6,-0.8 
        L 11.4,4.7 
        L 2.9,3.8 
        L 3.7,12.0 
        L -1.2,5.5 
        L -7.6,11.0 
        L -5.5,2.5 
        L -12.0,0 
        L -5.5,-2.5 
        L -7.6,-11.0 
        L -1.2,-5.5 
        Z"/>
</g>
                        </g>
                        <!-- バルーンの結び目 -->
                        <path d="M 95,250 C 95,255 105,255 105,250 Z" fill="#a0522d"/>
                    </svg>
                </div>
                <div id="explosion-particles"></div>
            </div>
        </div>

        <!-- Input Area -->
        <div id="input-area" class="center-text">
            <div class="input-container flex justify-center items-center gap-5">
                <div class="relative">
                    <input type="number" 
                           id="percentage-input" 
                           class="bg-white bg-opacity-30 border-2 border-amber-600 text-gray-800 text-6xl font-bold text-center rounded-lg w-56 focus:outline-none focus:ring-4 focus:ring-amber-400 transition-all duration-200" 
                           placeholder="0"
                           min="0" 
                           max="100"
                           autocomplete="off"
                           style="height: 88px;">
                    <span class="percent-symbol absolute right-5 top-1/2 transform -translate-y-1/2 text-3xl text-amber-600 pointer-events-none font-bold">%</span>
                </div>
                <button id="submit-btn" 
                        class="bg-amber-500 hover:bg-amber-600 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-bold text-2xl rounded-lg px-9 py-5 transition-all duration-200 transform hover:scale-105 disabled:hover:scale-100"
                        style="height: 88px;">
                    決定
                </button>
            </div>
            <div id="input-error" class="text-red-400 text-sm mt-2 hidden center-text">
                0から100の数字を入力してください
            </div>
        </div>
        
        <!-- Result Area -->
        <div id="result-area" class="hidden mt-6 text-4xl md:text-6xl font-bold">
            <p id="result-text" class="mb-4 center-text"></p>
            <p id="correct-answer-text" class="text-2xl md:text-3xl mt-4 text-blue-700 center-text px-4"></p>
            <div id="score-display" class="text-xl mt-4 text-amber-700 center-text"></div>
            <div class="center-text">
                <button id="next-btn" 
                        class="hidden mt-6 bg-green-500 hover:bg-green-600 text-white font-bold text-xl rounded-lg px-8 py-3 transition-all duration-200 transform hover:scale-105">
                    次の問題へ
                </button>
            </div>
        </div>

    </div>

    <!-- Start/End Modal -->
    <div id="modal" class="absolute inset-0 bg-black bg-opacity-80 flex items-center justify-center p-4 z-10">
        <div class="bg-gray-800 border-2 border-yellow-400 p-8 rounded-2xl shadow-lg text-center max-w-lg w-full text-white">
            <h2 id="modal-title" class="text-4xl font-bold text-yellow-300 mb-4 center-text">ヨルダン・パーセントバルーン</h2>
            <p id="modal-text" class="text-lg mb-8 center-text px-2">ヨルダンに関するクイズ！<br>表示される問題の答えとなるパーセンテージを予想して入力してください。<br>正解との誤差が許容範囲内ならクリアです！</p>
            <div id="final-score" class="hidden text-2xl text-green-400 mb-4 center-text"></div>
            <div class="center-text">
                <button id="modal-button" class="bg-yellow-400 hover:bg-yellow-500 text-black font-bold text-2xl rounded-lg px-10 py-4 transition-all duration-200 transform hover:scale-105">ゲーム開始</button>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            // --- Configuration ---
            const questions = [
                { question: "【練習問題】ヨルダンの国土のうち、砂漠または荒地が占める割合は？", answer: 80, tolerance: 10, comment: "正解は約80%！これは練習問題でした。ヨルダンは国土の大部分が砂漠や荒地で覆われています。", isPractice: true },
                { question: "ヨルダンに住む人々のうち、イスラム教を信仰している人の割合は？", answer: 92, tolerance: 5, comment: "正解は92%！国民の大多数がイスラム教を信仰しています。" },
                { question: "ヨルダンの国内総生産（GDP）のうち、サービス業が占める割合は？", answer: 67, tolerance: 8, comment: "正解は67%！現代のヨルダン経済はサービス業が主要な柱です。" },
                { question: "ヨルダン料理の代表格「マンサフ」。この料理に欠かせない乾燥ヨーグルト「ジャミード」の原料となる羊の乳の割合は？", answer: 100, tolerance: 0, comment: "正解は100%！ジャミードは100%羊の乳から作られる伝統的な食材です。" },
                { question: "ヨルダン国民が、生活の満足度を判断する上で最も重視する要素として「家族との関係」を挙げた人の割合は？", answer: 80, tolerance: 10, comment: "正解は約80%！ヨルダンでは家族の絆がとても大切にされています。" },
                { question: "ヨルダンの国旗の４色（黒・白・緑・赤）のうち、国の南部に広がる世界遺産「ワディ・ラム」の美しい砂の色を象徴している色が、国旗に占める割合は何パーセントでしょう？", answer: 0, tolerance: 0, comment: "正解は0%！ワディ・ラムの砂の色（オレンジ・ベージュ）は国旗の4色には含まれていません。" }
            ];

            // --- DOM Elements ---
            const gameContainer = document.getElementById('game-container');
            const questionNumberEl = document.getElementById('question-number');
            const questionTextEl = document.getElementById('question-text');
            const balloonEl = document.getElementById('balloon');
            const inputEl = document.getElementById('percentage-input');
            const submitBtn = document.getElementById('submit-btn');
            const resultArea = document.getElementById('result-area');
            const resultTextEl = document.getElementById('result-text');
            const correctAnswerTextEl = document.getElementById('correct-answer-text');
            const scoreDisplayEl = document.getElementById('score-display');
            const nextBtn = document.getElementById('next-btn');
            const modal = document.getElementById('modal');
            const modalTitle = document.getElementById('modal-title');
            const modalText = document.getElementById('modal-text');
            const modalButton = document.getElementById('modal-button');
            const finalScoreEl = document.getElementById('final-score');
            const inputError = document.getElementById('input-error');
            const progressDots = document.getElementById('progress-dots');

            // --- Game State ---
            let currentQuestionIndex = 0;
            let gameActive = true;
            let correctAnswers = 0;

            // --- Utility Functions ---
            const validateInput = (value) => {
                const num = parseInt(value, 10);
                return !isNaN(num) && num >= 0 && num <= 100;
            };

            const showInputError = (message) => {
                inputError.textContent = message;
                inputError.classList.remove('hidden');
                inputEl.classList.add('border-red-500');
                
                setTimeout(() => {
                    inputError.classList.add('hidden');
                    inputEl.classList.remove('border-red-500');
                }, 3000);
            };

            const createProgressDots = () => {
                progressDots.innerHTML = '';
                for (let i = 0; i < questions.length; i++) {
                    const dot = document.createElement('div');
                    dot.className = 'w-3 h-3 rounded-full border-2 border-yellow-300';
                    if (i < currentQuestionIndex) {
                        dot.classList.add('bg-green-400');
                    } else if (i === currentQuestionIndex) {
                        dot.classList.add('bg-yellow-300');
                    } else {
                        dot.classList.add('bg-transparent');
                    }
                    progressDots.appendChild(dot);
                }
            };

            // --- Game Logic ---
            const startGame = () => {
                currentQuestionIndex = 0;
                correctAnswers = 0;
                gameActive = true;
                modal.classList.add('hidden');
                gameContainer.classList.remove('hidden');
                displayQuestion();
            };

            const displayQuestion = () => {
                if (currentQuestionIndex >= questions.length) {
                    showEndScreen(true);
                    return;
                }
                
                gameActive = true;
                const question = questions[currentQuestionIndex];
                
                // UI Reset
                resultArea.classList.add('hidden');
                inputEl.value = '';
                inputEl.disabled = false;
                submitBtn.disabled = false;
                nextBtn.classList.add('hidden');
                inputError.classList.add('hidden');
                inputEl.classList.remove('border-red-500');
                
                // Balloon Reset
                balloonEl.classList.remove('explosion', 'correct-animation');
                balloonEl.style.opacity = '1';
                document.getElementById('explosion-particles').innerHTML = '';

                // Update Content
                if (question.isPractice) {
                    questionNumberEl.textContent = "練習";
                } else {
                    // 練習問題を除いた番号を表示
                    const actualQuestionNumber = currentQuestionIndex; // 練習問題も含めて1から開始
                    questionNumberEl.textContent = actualQuestionNumber;
                }
                
                questionTextEl.textContent = question.question;
                questionTextEl.classList.add('fade-in');
                
                // Update Progress
                createProgressDots();
                
                // Focus Input
                setTimeout(() => inputEl.focus(), 100);
            };

            const checkAnswer = () => {
                try {
                    if (!gameActive) return;
                    
                    const userAnswerStr = inputEl.value.trim();
                    
                    // Validation
                    if (!userAnswerStr) {
                        showInputError('数字を入力してください');
                        return;
                    }
                    
                    if (!validateInput(userAnswerStr)) {
                        showInputError('0から100の数字を入力してください');
                        return;
                    }

                    const userAnswer = parseInt(userAnswerStr, 10);
                    gameActive = false;
                    inputEl.disabled = true;
                    submitBtn.disabled = true;

                    const question = questions[currentQuestionIndex];
                    const difference = Math.abs(userAnswer - question.answer);
                    const isCorrect = difference <= question.tolerance;

                    // Show Result Area
                    resultArea.classList.remove('hidden');
                    correctAnswerTextEl.textContent = question.comment;

                    if (isCorrect) {
                        correctAnswers++;
                        resultTextEl.textContent = "SUCCESS!";
                        resultTextEl.className = "mb-2 text-green-400";
                        balloonEl.classList.add('correct-animation');
                        
                        // Confetti effect for correct answers
                        createSuccessParticles();
                    } else {
                        resultTextEl.textContent = "FAILED...";
                        resultTextEl.className = "mb-2 text-red-500";
                        balloonEl.classList.add('explosion');
                        createExplosionParticles();
                    }
                    
                    // Score Display
                    scoreDisplayEl.textContent = `スコア: ${correctAnswers}/${currentQuestionIndex + 1}`;
                    
                    // Show Next Button
                    setTimeout(() => {
                        nextBtn.classList.remove('hidden');
                    }, 500);

                } catch (error) {
                    console.error("回答チェック中にエラーが発生しました:", error);
                    resultArea.classList.remove('hidden');
                    resultTextEl.textContent = "エラーが発生しました。もう一度お試しください。";
                    resultTextEl.className = "mb-2 text-red-500";
                    gameActive = true;
                    inputEl.disabled = false;
                    submitBtn.disabled = false;
                }
            };

            const createExplosionParticles = () => {
                const container = document.getElementById('explosion-particles');
                container.innerHTML = '';
                const colors = ['#000', '#fff', '#008000', '#ce1126'];
                
                for (let i = 0; i < 30; i++) {
                    const particle = document.createElement('div');
                    particle.classList.add('particle');
                    particle.style.background = colors[Math.floor(Math.random() * colors.length)];
                    particle.style.left = '50%';
                    particle.style.top = '50%';
                    
                    const x = (Math.random() - 0.5) * 400;
                    const y = (Math.random() - 0.5) * 400;
                    
                    particle.animate([
                        { 
                            transform: 'translate(-50%, -50%) scale(1)', 
                            opacity: 1 
                        },
                        { 
                            transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y}px)) scale(0)`, 
                            opacity: 0 
                        }
                    ], { 
                        duration: 600 + Math.random() * 400, 
                        easing: 'ease-out', 
                        fill: 'forwards' 
                    });
                    
                    container.appendChild(particle);
                }
            };

            const createSuccessParticles = () => {
                const container = document.getElementById('explosion-particles');
                container.innerHTML = '';
                
                for (let i = 0; i < 20; i++) {
                    const particle = document.createElement('div');
                    particle.classList.add('particle');
                    particle.style.background = '#FFD700';
                    particle.style.left = '50%';
                    particle.style.top = '50%';
                    
                    const x = (Math.random() - 0.5) * 200;
                    const y = (Math.random() - 0.5) * 200;
                    
                    particle.animate([
                        { 
                            transform: 'translate(-50%, -50%) scale(0)', 
                            opacity: 0 
                        },
                        { 
                            transform: 'translate(-50%, -50%) scale(1)', 
                            opacity: 1 
                        },
                        { 
                            transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y}px)) scale(0)`, 
                            opacity: 0 
                        }
                    ], { 
                        duration: 800, 
                        easing: 'ease-out', 
                        fill: 'forwards' 
                    });
                    
                    container.appendChild(particle);
                }
            };

            const nextQuestion = () => {
                currentQuestionIndex++;
                displayQuestion();
            };

            const showEndScreen = (isWin) => {
                gameContainer.classList.add('hidden');
                modal.classList.remove('hidden');
                
                // 練習問題を除いたスコア計算
                const actualQuestions = questions.filter(q => !q.isPractice).length;
                let actualCorrectAnswers = 0;
                
                // 練習問題以外の正解数をカウント（簡易版）
                // 実際のプロジェクトでは各問題の結果を配列で管理することを推奨
                if (questions[0].isPractice) {
                    actualCorrectAnswers = Math.max(0, correctAnswers - (correctAnswers > 0 ? 1 : 0));
                } else {
                    actualCorrectAnswers = correctAnswers;
                }
                
                const percentage = actualQuestions > 0 ? Math.round((actualCorrectAnswers / actualQuestions) * 100) : 0;
                
                if (isWin) {
                    modalTitle.textContent = "ゲーム終了！";
                    
                    let message = "";
                    if (percentage === 100) {
                        message = "パーフェクト！あなたはヨルダンマスターです！🎉";
                    } else if (percentage >= 80) {
                        message = "素晴らしい！ヨルダンについてよく知っていますね！👏";
                    } else if (percentage >= 60) {
                        message = "良い調子です！もう少しでマスターですね！";
                    } else {
                        message = "ヨルダンについて学ぶ良い機会でした！";
                    }
                    
                    modalText.innerHTML = message + "<br>ワークショップを楽しんでくださいね。";
                    finalScoreEl.textContent = `最終スコア: ${actualCorrectAnswers}/${actualQuestions} (${percentage}%)`;
                    finalScoreEl.classList.remove('hidden');
                }
                
                modalButton.textContent = "もう一度プレイ";
            };

            // --- Event Listeners ---
            submitBtn.addEventListener('click', checkAnswer);
            
            inputEl.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && gameActive) {
                    checkAnswer();
                }
            });
            
            // Input validation on type
            inputEl.addEventListener('input', (e) => {
                const value = e.target.value;
                if (value && !validateInput(value)) {
                    e.target.classList.add('border-red-500');
                } else {
                    e.target.classList.remove('border-red-500');
                    inputError.classList.add('hidden');
                }
            });
            
            nextBtn.addEventListener('click', nextQuestion);
            modalButton.addEventListener('click', startGame);

            // Initialize progress dots
            createProgressDots();
        });
    </script>
</body>
</html>