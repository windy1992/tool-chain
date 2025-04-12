// 队列排队-1
let writeQueue = Promise.resolve();

function safeWrite(filePath, content) {
  writeQueue = writeQueue
    .then(() => {
      return fs.promises.writeFile(filePath, content);
    })
    .catch((err) => {
      console.error("Write error:", err);
    });
}

// 队列排队-2
const queue = [];

async function enqueue(task) {
  return await new Promise((resolve) => {
    queue.push(async () => {
      let result = await task();
      resolve(result);
    });
    if (queue.length === 1) runNext();
  });
}

async function runNext() {
  if (queue.length === 0) return;
  const task = queue[0];
  await task();
  queue.shift();
  runNext();
}

// 异步任务串行化
let isProcessing = false;

async function handleClick() {
  if (isProcessing) return; // 防重入
  isProcessing = true;

  await doSomethingAsync();

  isProcessing = false;
}
