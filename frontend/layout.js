// Star Office UI - 布局与层级配置
// 所有坐标、depth、资源路径统一管理在这里
// 避免 magic numbers，降低改错风险

// 核心规则：
// - 透明资源（如办公桌）强制 .png，不透明优先 .webp
// - 层级：低 → sofa(10) → starWorking(900) → desk(1000) → flower(1100)

const LAYOUT = {
  // === 游戏画布 ===
  game: {
    width: 1280,
    height: 720
  },

  // === 各区域坐标 ===
  areas: {
    door:        { x: 640, y: 550 },
    writing:     { x: 320, y: 360 },
    researching: { x: 350, y: 340 }, // 微调坐标，与 writing 错开，增加视觉区分度
    error:       { x: 1066, y: 180 },
    breakroom:   { x: 640, y: 360 }
  },

  // === 状态定义与文案 ===
  states: {
    idle: { name: '待命', area: 'breakroom' },
    writing: { name: '整理文档', area: 'writing' },
    researching: { name: '搜索信息', area: 'researching' },
    executing: { name: '执行任务', area: 'writing' },
    syncing: { name: '同步备份', area: 'writing' },
    error: { name: '出错了', area: 'error' }
  },

  // === 气泡对话库 ===
  bubbleTexts: {
    idle: [
      '待命中：耳朵竖起来了',
      '我在这儿，随时可以开工',
      '先把桌面收拾干净再说',
      '呼——给大脑放个风',
      '今天也要优雅地高效',
      '等待，是为了更准确的一击',
      '咖啡还热，灵感也还在',
      '我在后台给你加 Buff',
      '状态：静心 / 充电',
      '小猫说：慢一点也没关系'
    ],
    writing: [
      '进入专注模式：勿扰',
      '先把关键路径跑通',
      '我来把复杂变简单',
      '把 bug 关进笼子里',
      '写到一半，先保存',
      '把每一步都做成可回滚',
      '今天的进度，明天的底气',
      '先收敛，再发散',
      '让系统变得更可解释',
      '稳住，我们能赢'
    ],
    researching: [
      '我在挖证据链',
      '让我把信息熬成结论',
      '找到了：关键在这里',
      '先把变量控制住',
      '我在查：它为什么会这样',
      '把直觉写成验证',
      '先定位，再优化',
      '别急，先画因果图'
    ],
    executing: [
      '执行中：不要眨眼',
      '把任务切成小块逐个击破',
      '开始跑 pipeline',
      '一键推进：走你',
      '让结果自己说话',
      '先做最小可行，再做最美版本'
    ],
    syncing: [
      '同步中：把今天锁进云里',
      '备份不是仪式，是安全感',
      '写入中…别断电',
      '把变更交给时间戳',
      '云端对齐：咔哒',
      '同步完成前先别乱动',
      '把未来的自己从灾难里救出来',
      '多一份备份，少一份后悔'
    ],
    error: [
      '警报响了：先别慌',
      '我闻到 bug 的味道了',
      '先复现，再谈修复',
      '把日志给我，我会说人话',
      '错误不是敌人，是线索',
      '把影响面圈起来',
      '先止血，再手术',
      '我在：马上定位根因',
      '别怕，这种我见多了',
      '报警中：让问题自己现形'
    ],
    cat: [
      '喵~',
      '咕噜咕噜…',
      '尾巴摇一摇',
      '晒太阳最开心',
      '有人来看我啦',
      '我是这个办公室的吉祥物',
      '伸个腰',
      '今天的罐罐准备好了吗',
      '呼噜呼噜',
      '这个位置视野最好'
    ]
  },

  // === 装饰与家具：坐标 + 原点 + depth ===
  furniture: {
    // 沙发
    sofa: {
      x: 670,
      y: 144,
      origin: { x: 0, y: 0 },
      depth: 10
    },

    // 新办公桌（透明 PNG 强制）
    desk: {
      x: 218,
      y: 417,
      origin: { x: 0.5, y: 0.5 },
      depth: 1000
    },

    // 桌上花盆
    flower: {
      x: 310,
      y: 390,
      origin: { x: 0.5, y: 0.5 },
      depth: 1100,
      scale: 0.8
    },

    // Star 在桌前工作（在 desk 下面）
    starWorking: {
      x: 217,
      y: 333,
      origin: { x: 0.5, y: 0.5 },
      depth: 900,
      scale: 1.32
    },

    // 植物们
    plants: [
      { x: 565, y: 178, depth: 5 },
      { x: 230, y: 185, depth: 5 },
      { x: 977, y: 496, depth: 5 }
    ],

    // 海报
    poster: {
      x: 252,
      y: 66,
      depth: 4
    },

    // 咖啡机
    coffeeMachine: {
      x: 659,
      y: 397,
      origin: { x: 0.5, y: 0.5 },
      depth: 99
    },

    // 服务器区
    serverroom: {
      x: 1021,
      y: 142,
      origin: { x: 0.5, y: 0.5 },
      depth: 2
    },

    // 错误 bug
    errorBug: {
      x: 1007,
      y: 221,
      origin: { x: 0.5, y: 0.5 },
      depth: 50,
      scale: 0.9,
      pingPong: { leftX: 1007, rightX: 1111, speed: 0.6 }
    },

    // 同步动画
    syncAnim: {
      x: 1157,
      y: 592,
      origin: { x: 0.5, y: 0.5 },
      depth: 40
    },

    // 小猫
    cat: {
      x: 94,
      y: 557,
      origin: { x: 0.5, y: 0.5 },
      depth: 2000
    }
  },

  // === 牌匾 ===
  plaque: {
    x: 640,
    y: 720 - 36,
    width: 420,
    height: 44
  },

  // === 资源加载规则：哪些强制用 PNG（透明资源） ===
  forcePng: {
    desk_v2: true // 新办公桌必须透明，强制 PNG
  },

  // === 总资源数量（用于加载进度条） ===
  totalAssets: 15
};
