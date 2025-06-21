<template>
  <!-- 右上角固定按钮 -->
  <div class="cloze-button" @click="openCloze">
    <i class="fas fa-pen"></i>
  </div>
  
  <!-- 完形填空弹窗 -->
  <div class="cloze-overlay" :class="{ active: showCloze }">
    <div class="cloze-container">
      <div class="cloze-header">
        <h2><i class="fas fa-edit"></i> 日语完形填空练习</h2>
        <button class="close-btn" @click="closeCloze">
          <i class="fas fa-times"></i>×
        </button>
      </div>
      
      <div class="cloze-content">
        <!-- 左侧：文章区域 -->
        <div class="article-section">
          <h3 class="article-title"><i class="fas fa-book"></i> {{ title }}</h3>
          <div class="article-content-wrapper">
            <div class="article-content" id="articleContent">
              <template v-for="(part, index) in articleParts" :key="index">
                <span v-if="index % 2 === 0">{{ part }}</span>
                <div v-else 
                class="blank" 
                :class="{
                    filled: userAnswers[part] !== undefined,
                    correct: showResults && isAnswerCorrect(part),
                    incorrect: showResults && !isAnswerCorrect(part),
                    'drop-target': dragOverBlank === part
                }"
                :data-id="part"
                @dragover.prevent="handleDragOver($event, part)" 
                @dragleave="dragOverBlank = null"
                @drop="handleDrop($event, part)"
                >
                    <span class="blank-number">{{ parseInt(part) + 1 }}</span>
                    <span v-if="userAnswers[part] !== undefined">{{ getOptionText(userAnswers[part]) }}</span>
                
                    <!-- 添加清空按钮 -->
                    <button v-if="userAnswers[part]" class="clear-btn" @click.stop="clearBlank(part)">
                        <i class="fas fa-times"></i>×
                    </button>
                </div>
              </template>
            </div>
          </div>
        </div>
        
        <!-- 右侧：选项区域 -->
        <div class="options-section">
          <h3 class="options-title"><i class="fas fa-list"></i> 选项</h3>
          <div class="stats-container">
            <span>已填: {{ filledCount }}/{{ totalBlanks }}</span>
            <span>正确率: {{ accuracy }}%</span>
          </div>
          <div class="options-scroll-container" 
            :class="{ 'drop-over': isOptionAreaDropOver }"
            @dragover.prevent="handleOptionAreaDragover"
            @dragenter="isOptionAreaDropOver = true"
            @dragleave="isOptionAreaDropOver = false"
            @drop="handleOptionAreaDrop">
                <div class="options-list">
                <div 
                    v-for="option in options" 
                    :key="option.id"
                    class="option" 
                    :class="{ used: isOptionUsed(option.id) }"
                    draggable="true"
                    @dragstart="handleDragStart($event, option.id)"
                >
                    <div class="option-jp">{{ option.jp }}</div>
                    <div v-if="showResults" class="option-zh">{{ option.zh }}</div>
                </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="cloze-footer">
        <button 
          class="complete-btn" 
          :disabled="!isComplete || showResults"
          @click="checkAnswers"
        >
          <i class="fas fa-check-circle"></i> 完成
        </button>
        
        <div class="result-section" v-if="showResults">
          <div 
            v-for="blank in blanks" 
            :key="blank.id"
            class="result-item" 
            :class="isAnswerCorrect(blank.id) ? 'correct' : 'incorrect'"
          >
            <div class="result-icon">{{ isAnswerCorrect(blank.id) ? '✓' : '✗' }}</div>
            <div class="result-text">
              <strong>空格 {{ blank.id + 1 }}:</strong> 
              {{ getOptionText(userAnswers[blank.id]) }} ({{ getOptionZh(userAnswers[blank.id]) }})
              <span v-if="!isAnswerCorrect(blank.id)" style="color:#3498db;">
                <br>正确答案: {{ getCorrectOptionText(blank.id) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import api from "@/api";

export default {
  name: 'ClozeGenerator',
  setup() {
    // 状态管理
    const showCloze = ref(false);
    const vocabulary = ref([]);
    const clozeData = ref(null);
    const userAnswers = ref({});
    const showResults = ref(false);
    const dragOverBlank = ref(null); // 当前拖拽悬停的空白ID
    const draggedOption = ref(null); // 当前拖拽的选项ID
    const isOptionAreaDropOver = ref(false); // 选项区域是否处于拖拽悬停状态
    
    // 配置参数
    const wordCount = ref(5);
    const correctRatio = ref(0.3);
    
    // 加载词汇数据
    const loadVocabulary = async () => {
      try {
        const response = await fetch('/public/note/vocabulary.json');
        vocabulary.value = await response.json();
      } catch (error) {
        console.error('加载词汇数据失败:', error);
        // 使用示例数据作为后备
        vocabulary.value = [
          { id: 1, jp: "散歩しました", zh: "散步了", correct_judge: 1 },
          // ...其他词汇
        ];
      }
    };
    
    // 从词汇表中随机选择单词
    const selectRandomWords = (count, ratio) => {
        console.log('vocabulary',vocabulary.value)
      // 分离正确和错误的词汇
      const correctWords = vocabulary.value.filter(word => word.correct_judge === 1);
      const incorrectWords = vocabulary.value.filter(word => word.correct_judge === 0);
      
      // 计算需要选择的正确单词数量
      const correctCount = Math.round(count * ratio);
      const incorrectCount = count - correctCount;
      
      // 随机选择单词
      const selected = [];
      
      // 选择正确单词
      for (let i = 0; i < correctCount && correctWords.length > 0; i++) {
        const randomIndex = Math.floor(Math.random() * correctWords.length);
        selected.push(correctWords.splice(randomIndex, 1)[0]);
      }
      
      // 选择错误单词
      for (let i = 0; i < incorrectCount && incorrectWords.length > 0; i++) {
        const randomIndex = Math.floor(Math.random() * incorrectWords.length);
        selected.push(incorrectWords.splice(randomIndex, 1)[0]);
      }
      
      // 如果数量不足，补充随机单词
      if (selected.length < count) {
        const remaining = vocabulary.value.filter(word => !selected.includes(word));
        const needed = count - selected.length;
        for (let i = 0; i < needed && remaining.length > 0; i++) {
          const randomIndex = Math.floor(Math.random() * remaining.length);
          selected.push(remaining.splice(randomIndex, 1)[0]);
        }
      }
      
      // 打乱顺序
      return selected.sort(() => Math.random() - 0.5);
    };

    // 生成完形填空内容
    const generateCloze = async () => {
        if (vocabulary.value.length === 0){
        alert('没有学到新词呢，请先去学习新词吧');
        closeCloze()
        return
      }
      // 选择单词
      const wordList = selectRandomWords(wordCount.value, correctRatio.value);
      
      // 背景故事（固定）
      const background = "在江户时代的日本，武士阶层统治着社会。普通百姓生活简朴，商人阶层开始崛起。";
      
            try {
           const response = await api.post("/cloze/generate", {
          background_story: background,
          word_list: wordList,
          count: 1,
        });

           //const data = await response.json();
           
          
          // 模拟API响应数据
          //const data = {
          //  title: "江户时代的社会",
          //  content: "在江户时代的日本，[0]统治着社会。普通百姓生活[1]，[2]阶层开始崛起。",
          //  blanks: [
          //    { id: 0, correctOptionId: 0 },
          //    { id: 1, correctOptionId: 1 },
          //    { id: 2, correctOptionId: 2 }
          //  ],
          //  options: wordList.map((word, index) => ({
          //    id: index,
          //    jp: word.jp,
          //    zh: word.zh
          //  }))
          //};
          
          //clozeData = data;

          clozeData.value = response.data;
          return initClozeTest();
        } catch (error) {
          console.error('生成完形填空失败:', error);
          alert('生成完形填空失败，请重试！');
        }
        
      }
    
    // 初始化完形填空
    const initClozeTest = () => {
        // 重置用户答案和结果状态
        userAnswers.value = {};
        showResults.value = false;

        // Fisher-Yates洗牌算法
        const shuffleArray = (array) => {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
        };

        // 创建选项副本并打乱顺序
        const shuffledOptions = shuffleArray([...clozeData.value.options]);

        // 创建原始ID到新位置的映射
        const optionIdToIndexMap = {};
        shuffledOptions.forEach((option, index) => {
        optionIdToIndexMap[option.id] = index;
        });

        // 更新空白区域的正确选项ID为新的索引位置
        const updatedBlanks = clozeData.value.blanks.map(blank => {
        const originalOptionId = blank.correctOptionId;
        return {
            ...blank,
            correctOptionId: optionIdToIndexMap[originalOptionId]
        };
        });

        // 更新组件数据
        clozeData.value = {
        ...clozeData.value,
        options: shuffledOptions,
        blanks: updatedBlanks
        }
        console.log(clozeData.value)
        return clozeData.value
        };
      
    // 打开完形填空弹窗
    const openCloze = async () => {
      showCloze.value = true;
      //if (!vocabulary.value.length) {
        await loadVocabulary();
      //}
      clozeData.value = await generateCloze();
      userAnswers.value = {};
      showResults.value = false;
    };
    
    // 关闭完形填空弹窗
    const closeCloze = () => {
      showCloze.value = false;
      showResults.value = false;
      //清空数据
      clozeData.value = null;
    };
    
    // 处理拖拽开始
    const handleDragStart = (e, optionId) => {
        e.dataTransfer.setData('optionId', optionId);
        draggedOption.value = parseInt(optionId); // 记录当前拖拽的选项
    };
    
    // 处理拖拽放置
    const handleDrop = (e, blankId) => {
        e.preventDefault();
        dragOverBlank.value = null;
        
        const optionId = e.dataTransfer.getData('optionId');
        const blankIdNum = parseInt(blankId);
        const optionIdNum = parseInt(optionId);
        
        // 更新答案
        userAnswers.value = {
            ...userAnswers.value,
            [blankIdNum]: optionIdNum
        };
        
        // 如果选项是从其他空白拖来的，移除原位置
        Object.keys(userAnswers.value).forEach(id => {
            const idNum = parseInt(id);
            if (idNum !== blankIdNum && userAnswers.value[idNum] === optionIdNum) {
            const newAnswers = {...userAnswers.value};
            delete newAnswers[idNum];
            userAnswers.value = newAnswers;
            }
        });
        
        draggedOption.value = null;
    };

    // 检查选项是否已被使用
    const isOptionUsed = (optionId) => {
      return Object.values(userAnswers.value).includes(optionId);
    };
    
    // 检查答案是否正确
    const isAnswerCorrect = (blankId) => {
      if (!clozeData.value || !showResults.value) return false;
      const blank = clozeData.value.blanks.find(b => b.id === parseInt(blankId));
      return blank && userAnswers.value[blankId] === blank.correctOptionId;
    };

    // 添加拖拽悬停效果处理
    const handleDragOver = (e, blankId) => {
    e.preventDefault();
    dragOverBlank.value = blankId;
    };

    // 添加选项区域拖拽悬停处理
    const handleOptionAreaDragover = (e) => {
    e.preventDefault();
    isOptionAreaDropOver.value = true;
    };
   
    // 添加选项区域放置处理（撤回）
    const handleOptionAreaDrop = (e) => {
    e.preventDefault();
    isOptionAreaDropOver.value = false;
    
    if (!draggedOption.value) return;
    
    // 找到并移除该选项的所有空白
    Object.keys(userAnswers.value).forEach(blankId => {
        const blankIdNum = parseInt(blankId);
        if (userAnswers.value[blankIdNum] === draggedOption.value) {
        const newAnswers = {...userAnswers.value};
        delete newAnswers[blankIdNum];
        userAnswers.value = newAnswers;
        }
    });
    
    draggedOption.value = null;
    };

    // 添加清空按钮处理
    const clearBlank = (blankId) => {
        const blankIdNum = parseInt(blankId);
        const newAnswers = {...userAnswers.value};
        delete newAnswers[blankIdNum];
        userAnswers.value = newAnswers;
    };
    
    // 获取选项文本
    const getOptionText = (optionId) => {
      if (!clozeData.value) return '';
      const option = clozeData.value.options.find(o => o.id === optionId);
      return option ? option.jp : '';
    };
    
    // 获取选项中文
    const getOptionZh = (optionId) => {
      if (!clozeData.value) return '';
      const option = clozeData.value.options.find(o => o.id === optionId);
      return option ? option.zh : '';
    };
    
    // 获取正确答案文本
    const getCorrectOptionText = (blankId) => {
      if (!clozeData.value) return '';
      const blank = clozeData.value.blanks.find(b => b.id === parseInt(blankId));
      if (!blank) return '';
      const option = clozeData.value.options.find(o => o.id === blank.correctOptionId);
      return option ? `${option.jp} (${option.zh})` : '';
    };
    
    // 检查答案
    const checkAnswers = () => {
      showResults.value = true;
    };
    
    // 计算属性
    const articleParts = computed(() => {
      if (!clozeData.value) return ['加载中...'];
      return clozeData.value.content.split(/\[(\d+)\]/g);
    });
    
    const blanks = computed(() => {
      return clozeData.value?.blanks || [];
    });
    
    const options = computed(() => {
      return clozeData.value?.options || [];
    });
    
    const filledCount = computed(() => {
      return Object.keys(userAnswers.value).length;
    });
    
    const totalBlanks = computed(() => {
      return clozeData.value?.blanks?.length || 0;
    });
    
    const isComplete = computed(() => {
      return filledCount.value === totalBlanks.value;
    });
    
    const accuracy = computed(() => {
      if (!showResults.value || !clozeData.value) return 0;
      
      let correctCount = 0;
      for (const blank of clozeData.value.blanks) {
        if (userAnswers.value[blank.id] === blank.correctOptionId) {
          correctCount++;
        }
      }
      
      return totalBlanks.value > 0 
        ? Math.round((correctCount / totalBlanks.value) * 100)
        : 0;
    });

    const title = computed(() => {
      return clozeData.value?.title || '中文文章';
    });
    
    // 初始化加载词汇
    onMounted(loadVocabulary);
    
    return {
      showCloze,
      openCloze,
      closeCloze,
      handleDragStart,
      handleDrop,
      isOptionUsed,
      isAnswerCorrect,
      getOptionText,
      getOptionZh,
      getCorrectOptionText,
      checkAnswers,
      handleDragOver,
      handleOptionAreaDragover,
      handleOptionAreaDrop,
      clearBlank,
      dragOverBlank,
      isOptionAreaDropOver,
      articleParts,
      blanks,
      options,
      title,
      userAnswers,
      showResults,
      filledCount,
      totalBlanks,
      isComplete,
      accuracy,
      wordCount,
      correctRatio
    };
  }
};
</script>

<style scoped>
/* 右上角按钮 */
.cloze-button {
  position: fixed;
  top: 210px;
  right: 45px;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #ff9966, #ff5e62);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  color: white;
  font-size: 1.8rem;
  border: 3px solid white;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.cloze-button:hover {
  transform: scale(1.05);
}

/* 完形填空弹窗 */
.cloze-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

.cloze-overlay.active {
  opacity: 1;
  pointer-events: all;
}

.cloze-container {
  background: white;
  width: 90%;
  max-width: 1000px;
  height: 85vh;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transform: scale(0.95);
  transition: transform 0.3s ease;
  overflow-y: auto;
}

.cloze-overlay.active .cloze-container {
  transform: scale(1);
}

/* 弹窗头部 */
.cloze-header {
  background: linear-gradient(to right, #3a7bd5, #00d2ff);
  color: white;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 2.0rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.close-btn:hover {
  transform: rotate(90deg);
}

/* 内容区域 */
.cloze-content {
  display: flex;
  flex: 1;
  min-height: 65%;
  padding: 20px;
  gap: 20px;
  overflow: hidden;
}

/* 左侧文章区域 */
.article-section {
  flex: 1;
  background: #f9f9f9;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.article-title {
  font-size: 1.3rem;
  margin-bottom: 15px;
  color: #2c3e50;
  padding-bottom: 10px;
  border-bottom: 2px solid #3498db;
}

.article-content-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background: white;
  border-radius: 8px;
  border: 1px solid #eee;
}

.article-content {
  font-size: 1.1rem;
  line-height: 1.7;
  text-align: justify;
}

/* 右侧选项区域 */
.options-section {
  flex: 0 0 280px;
  background: #f9f9f9;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.options-title {
  font-size: 1.3rem;
  margin-bottom: 15px;
  color: #2c3e50;
  padding-bottom: 10px;
  border-bottom: 2px solid #3498db;
}

.options-scroll-container {
  flex: 1;
  overflow-y: auto;
  padding: 5px;
}

/* 滚动条样式 */
.article-content-wrapper::-webkit-scrollbar,
.options-scroll-container::-webkit-scrollbar {
  width: 8px;
}

.article-content-wrapper::-webkit-scrollbar-track,
.options-scroll-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.article-content-wrapper::-webkit-scrollbar-thumb,
.options-scroll-container::-webkit-scrollbar-thumb {
  background: #3498db;
  border-radius: 4px;
}

/* 空白区域样式 */
.blank {
  display: inline-block;
  min-width: 80px;
  height: 36px;
  border: 2px dashed #3498db;
  border-radius: 6px;
  margin: 0 4px;
  vertical-align: middle;
  background: #f8f9fa;
  position: relative;
  text-align: center;
  line-height: 32px;
  font-size: 0.9rem;
  color: #555;
}

.blank.filled {
  border-style: solid;
  background: #e3f2fd;
  color: #333;
  font-weight: bold;
}

.blank.correct {
  border-color: #2ecc71;
  background: rgba(46, 204, 113, 0.1);
}

.blank.incorrect {
  border-color: #e74c3c;
  background: rgba(231, 76, 60, 0.1);
}

.blank-number {
  position: absolute;
  top: -18px;
  left: 5px;
  font-size: 0.75rem;
  color: #7f8c8d;
}

/* 空白区域悬停效果 */
.blank:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* 添加拖拽目标效果 */
.blank.drop-target {
  box-shadow: 0 0 10px rgba(52, 152, 219, 0.7);
  transform: scale(1.05);
  transition: all 0.2s ease;
}

/* 选项样式 */
.option {
  background: #e3f2fd;
  border: 2px solid #3498db;
  border-radius: 8px;
  padding: 10px 12px;
  margin-bottom: 10px;
  cursor: grab;
  transition: all 0.3s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.95rem;
}

.option:hover {
  background: #bbdefb;
  transform: translateY(-3px);
  box-shadow: 0 3px 8px rgba(0,0,0,0.1);
}

.option:active {
  cursor: grabbing;
}

.option.used {
  opacity: 0.5;
  background: #f5f5f5;
  cursor: not-allowed;
}

.option-jp {
  font-weight: bold;
  flex: 1;
}

.option-zh {
  color: #7f8c8d;
  font-size: 0.85rem;
  margin-left: 10px;
}

/* 选项区域放置反馈 */
.options-scroll-container.drop-over {
  background: rgba(52, 152, 219, 0.1);
  border: 2px dashed #3498db;
}

/* 添加清空按钮 */
.clear-btn {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 20px;
  height: 20px;
  background: #e74c3c;
  border-radius: 50%;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 0.7rem;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.3s ease;
  border: none;
  z-index: 10;
}

.blank:hover .clear-btn {
  opacity: 1;
}

/* 底部区域 */
.cloze-footer {
  padding: 15px 20px;
  background: #f8f9fa;
  border-top: 2px solid #e9ecef;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.complete-btn {
  background: linear-gradient(to right, #27ae60, #2ecc71);
  color: white;
  border: none;
  padding: 10px 25px;
  border-radius: 50px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.complete-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.25);
}

.complete-btn:disabled {
  background: #95a5a6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* 统计信息 */
.stats-container {
  display: flex;
  justify-content: space-between;
  margin: 10px 0;
  font-size: 0.9rem;
  color: #555;
}

/* 结果区域 */
.result-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 200px;
  overflow-y: auto;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 10px;
  border: 1px solid #e9ecef;
}

.result-item {
  padding: 8px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
}

.result-item.correct {
  background: rgba(46, 204, 113, 0.1);
  border-left: 4px solid #2ecc71;
}

.result-item.incorrect {
  background: rgba(231, 76, 60, 0.1);
  border-left: 4px solid #e74c3c;
}

.result-icon {
  font-size: 1.1rem;
}

.result-text {
  flex: 1;
}

.instructions h3 {
  margin-bottom: 8px;
  color: #e67e22;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
}

.instructions p {
  line-height: 1.5;
}

/* 响应式设计 */
@media (max-width: 900px) {
  .cloze-content {
    flex-direction: column;
  }
  
  .article-section, .options-section {
    width: 100%;
  }
  
  .options-section {
    flex: 0 0 auto;
    height: 40vh;
  }
}
</style>