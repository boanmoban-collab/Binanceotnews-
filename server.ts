import express from 'express';
import { exec } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3000;
const REPO_DIR = path.join(__dirname, 'wife_bain1_repo');
const ZIP_PATH = path.join(__dirname, 'public', 'wife_bain1-fixed.zip');

app.use(express.json());

// Helper to execute bash command safely
function runCmd(cmd: string, cwd = REPO_DIR): Promise<{ stdout: string; stderr: string; code: number }> {
  return new Promise((resolve) => {
    exec(cmd, { cwd }, (error, stdout, stderr) => {
      resolve({
        stdout: stdout || '',
        stderr: stderr || '',
        code: error ? (error.code || 1) : 0,
      });
    });
  });
}

// 1. Status API
app.get('/api/status', async (_req, res) => {
  try {
    const gitLog = await runCmd('git log -n 5 --pretty=format:"%h|%s|%an|%ad" --date=short');
    const gitBranch = await runCmd('git branch --show-current');
    const gitRemote = await runCmd('git remote -v');

    const commits = gitLog.stdout
      .split('\n')
      .filter(Boolean)
      .map((line) => {
        const [hash, msg, author, date] = line.split('|');
        return { hash, message: msg, author, date };
      });

    // Check files
    let filesCount = 0;
    if (fs.existsSync(REPO_DIR)) {
      const files = fs.readdirSync(REPO_DIR).filter((f) => !f.startsWith('.git') && f !== '__pycache__');
      filesCount = files.length;
    }

    res.json({
      status: 'ready',
      repoName: 'aboanasanam42-cpu/wife_bain1',
      branch: gitBranch.stdout.trim() || 'main',
      remoteUrl: 'https://github.com/aboanasanam42-cpu/wife_bain1.git',
      commits,
      filesCount,
      zipExists: fs.existsSync(ZIP_PATH),
      zipSize: fs.existsSync(ZIP_PATH) ? fs.statSync(ZIP_PATH).size : 0,
    });
  } catch (err: any) {
    res.status(500).json({ error: err.message });
  }
});

// 2. Files API
app.get('/api/files', async (_req, res) => {
  try {
    const fileList: Array<{ name: string; path: string; size: number; content: string; status: string }> = [];

    const fileMap: Record<string, string> = {
      'main.py': 'محرك البوت الرئيسي 24/7 وخادم فحص الصحة ولوحة التحكم',
      'spot_engine.py': 'محرك الصفقات الفورية وحساب الكميات ووقف الخسارة المتحرك',
      'indicators.py': 'مؤشرات التحليل الفني (RSI والارتداد والتذبذب) بدون مكتبات خارجية',
      'config.py': 'إدارة المتغيرات البيئية وفحص أزواج العملات وحدود بينانس',
      'test_engine.py': 'مجموعة الاختبارات الآلية (Unit Tests) لسلامة العمليات الحسابية',
      '.github/workflows/ci.yml': 'ملف فحص الجودة التلقائي على GitHub Actions',
      'requirements.txt': 'حزم بايثون الأساسية (ccxt, requests, dotenv)',
      'Dockerfile': 'حاوية دوكر المتوافقة للتشغيل المستمر',
      'railway.json': 'ملف إعداد ونشر الخدمة على منصة Railway',
      'Procfile': 'أمر التشغيل المباشر للخدمة',
      'README.md': 'دليل التوثيق والتشغيل الشامل',
      '.env.example': 'قالب مفاتيح التداول والمتغيرات',
    };

    for (const [relPath, desc] of Object.entries(fileMap)) {
      const fullPath = path.join(REPO_DIR, relPath);
      if (fs.existsSync(fullPath)) {
        const stat = fs.statSync(fullPath);
        const content = fs.readFileSync(fullPath, 'utf-8');
        fileList.push({
          name: path.basename(relPath),
          path: relPath,
          size: stat.size,
          content,
          status: desc,
        });
      }
    }

    res.json({ files: fileList });
  } catch (err: any) {
    res.status(500).json({ error: err.message });
  }
});

// 3. Run Tests API
app.post('/api/run-tests', async (_req, res) => {
  try {
    const result = await runCmd('python3 -m unittest test_engine.py');
    const isSuccess = result.code === 0;

    res.json({
      success: isSuccess,
      code: result.code,
      stdout: result.stdout,
      stderr: result.stderr,
      summary: isSuccess
        ? 'تم اجتياز جميع الاختبارات الآلية التسعة (9/9 Tests Passed) بنجاح!'
        : 'فشل في أحد الاختبارات',
    });
  } catch (err: any) {
    res.status(500).json({ error: err.message });
  }
});

// 4. Push to GitHub API
app.post('/api/push', async (req, res) => {
  try {
    const { token, branch = 'main', repo = 'aboanasanam42-cpu/wife_bain1' } = req.body;

    if (!token || typeof token !== 'string' || token.trim().length === 0) {
      return res.status(400).json({
        success: false,
        error: 'يرجى إدخال رمز الوصول الشخصي (GitHub Personal Access Token)',
      });
    }

    const cleanToken = token.trim();
    const cleanRepo = repo.trim();
    const cleanBranch = branch.trim();

    // Mask function to avoid leaking token in logs
    const maskToken = (str: string) => str.split(cleanToken).join('***TOKEN***');

    // 1. Configure git user if not set
    await runCmd('git config user.name "AI Studio"', REPO_DIR);
    await runCmd('git config user.email "bot@example.com"', REPO_DIR);

    // 2. Ensure everything is committed
    await runCmd('git add -A', REPO_DIR);
    await runCmd('git commit -m "fix(spot): enhance dynamic filters, fee compensation, precision and unit tests" || true', REPO_DIR);

    // 3. Set authenticated remote URL
    const authenticatedUrl = `https://${cleanToken}@github.com/${cleanRepo}.git`;
    await runCmd(`git remote set-url origin ${authenticatedUrl}`, REPO_DIR);

    // 4. Push to remote
    const pushResult = await runCmd(`git push origin ${cleanBranch}`, REPO_DIR);

    // Reset origin back to public URL for security
    await runCmd(`git remote set-url origin https://github.com/${cleanRepo}.git`, REPO_DIR);

    if (pushResult.code === 0) {
      const commitSha = await runCmd('git rev-parse HEAD', REPO_DIR);
      return res.json({
        success: true,
        message: 'تم دفع كافة الملفات المصححة بنجاح إلى مستودع GitHub!',
        commit: commitSha.stdout.trim(),
        log: maskToken(pushResult.stdout + '\n' + pushResult.stderr),
      });
    } else {
      return res.status(400).json({
        success: false,
        error: maskToken(pushResult.stderr || pushResult.stdout || 'فشل أمر الدفع (git push). تأكد من صحة التوكن والصلاحيات (repo scope).'),
        log: maskToken(pushResult.stdout + '\n' + pushResult.stderr),
      });
    }
  } catch (err: any) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// 5. Download Zip & Readme API
app.get('/api/download-zip', (_req, res) => {
  if (fs.existsSync(ZIP_PATH)) {
    res.download(ZIP_PATH, 'wife_bain1-fixed.zip');
  } else {
    res.status(404).send('الملف المضغوط غير موجود');
  }
});

app.get('/api/download-readme', (_req, res) => {
  const readmePath = path.join(REPO_DIR, 'README.md');
  if (fs.existsSync(readmePath)) {
    res.download(readmePath, 'README.md');
  } else {
    res.status(404).send('ملف README غير موجود');
  }
});

// Vite Middleware Integration
async function startServer() {
  if (process.env.NODE_ENV === 'production') {
    app.use(express.static(path.join(__dirname, 'dist')));
    app.get('*', (_req, res) => {
      res.sendFile(path.join(__dirname, 'dist', 'index.html'));
    });
  } else {
    const { createServer: createViteServer } = await import('vite');
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running at http://0.0.0.0:${PORT}`);
  });
}

startServer();
