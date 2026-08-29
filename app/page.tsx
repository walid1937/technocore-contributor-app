"""use client";

import React, { useState, useEffect } from 'react';
import { CheckCircle2, XCircle, Terminal, Download, ShieldAlert, Key, Copy, Check, Twitter, ArrowRight } from 'lucide-react';

export default function TechnocoreApp() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState({
    passphrase: '',
    did: 'did:key:z6Mksquga7BbhDEjS6xdexNiaTHa5cnMPozUn6tfqJF5imgz',
    repoUrl: 'https://github.com/zunmax/technocore-did-starter',
    commit: '3cc03a6e908e8776de9fdd465c53d23d31db2e9f',
    copied: false
  });

  const nextStep = () => setStep(s => s + 1);

  const simulateProcess = (time: number, callback: () => void) => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      callback();
    }, time);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setData({ ...data, copied: true });
    setTimeout(() => setData({ ...data, copied: false }), 2000);
  };

  const Step1Welcome = () => (
    <div className="text-center space-y-6">
      <h1 className="text-3xl font-bold text-white">Welcome to Technocore Contributor</h1>
      <p className="text-gray-300 max-w-md mx-auto">
        This app helps you create your Technocore DID, make a signed contribution, create proof of your contribution, and verify it.
        <br/><br/>
        <span className="text-green-400 font-semibold">You don't need to know Python or Git.</span>
      </p>
      <button onClick={nextStep} className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-bold transition">
        Start Setup
      </button>
    </div>
  );

  const Step2SysCheck = () => {
    const [checks, setChecks] = useState(0);
    useEffect(() => {
      if (checks < 4) {
        const timer = setTimeout(() => setChecks(c => c + 1), 600);
        return () => clearTimeout(timer);
      }
    }, [checks]);

    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-white mb-4">System Check</h2>
        <div className="space-y-3 bg-gray-900 p-6 rounded-lg font-mono text-sm">
          <div className="flex items-center text-gray-300">
            {checks > 0 ? <CheckCircle2 className="w-5 h-5 text-green-500 mr-2" /> : <span className="w-5 h-5 mr-2 animate-pulse bg-gray-600 rounded-full" />}
            Windows 10/11 (64-bit)
          </div>
          <div className="flex items-center text-gray-300">
            {checks > 1 ? <CheckCircle2 className="w-5 h-5 text-green-500 mr-2" /> : <span className="w-5 h-5 mr-2 animate-pulse bg-gray-600 rounded-full" />}
            Internet connection verified
          </div>
          <div className="flex items-center text-gray-300">
            {checks > 2 ? <CheckCircle2 className="w-5 h-5 text-green-500 mr-2" /> : <span className="w-5 h-5 mr-2 animate-pulse bg-gray-600 rounded-full" />}
            Python 3.12.10 detected (✅ Compatible)
          </div>
          <div className="flex items-center text-gray-300">
            {checks > 3 ? <CheckCircle2 className="w-5 h-5 text-green-500 mr-2" /> : <span className="w-5 h-5 mr-2 animate-pulse bg-gray-600 rounded-full" />}
            Git 2.x.x detected (✅ Ready)
          </div>
        </div>
        <p className="text-sm text-gray-400 text-center">Python runs the tool. Git manages the project files.</p>
        <button onClick={nextStep} disabled={checks < 4} className="w-full bg-blue-600 disabled:bg-gray-600 text-white px-4 py-3 rounded-lg font-bold transition">
          Continue
        </button>
      </div>
    );
  };

  const Step3Download = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white">Download Starter</h2>
      <div className="bg-gray-900 p-6 rounded-lg text-gray-300 font-mono text-sm space-y-4">
        <p className="text-blue-400">Repository:</p>
        <p>github.com/zunmax/technocore-did-starter</p>
        <p className="text-blue-400">Location:</p>
        <p>C:\Users\USERNAME\Technocore</p>
      </div>
      <button 
        onClick={() => simulateProcess(1500, nextStep)} 
        disabled={loading}
        className="w-full bg-blue-600 text-white px-4 py-3 rounded-lg font-bold flex justify-center items-center gap-2"
      >
        {loading ? <span className="animate-pulse">Downloading...</span> : <><Download className="w-5 h-5"/> Download Repository</>}
      </button>
    </div>
  );

  const Step4Env = () => {
    useEffect(() => { simulateProcess(2000, nextStep) }, []);
    return (
      <div className="space-y-6 text-center">
        <Terminal className="w-12 h-12 text-blue-500 mx-auto animate-pulse" />
        <h2 className="text-2xl font-bold text-white">Preparing Environment</h2>
        <div className="bg-gray-900 p-4 rounded-lg text-left font-mono text-green-400 text-sm">
          <p>{">"} py -3.12 -m venv .venv</p>
          <p>{">"} python -m pip install --upgrade pip</p>
          <p>{">"} python -m pip install -r requirements.txt</p>
          <p className="mt-2 text-gray-400">Please wait while we configure Python...</p>
        </div>
      </div>
    );
  };

  const Step5CreateDID = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white">Create Identity Passphrase</h2>
      <div className="bg-orange-900/30 border border-orange-500/50 p-4 rounded-lg flex gap-3 text-orange-200 text-sm">
        <ShieldAlert className="w-6 h-6 flex-shrink-0" />
        <div>
          <p className="font-bold mb-1">Important: This protects your identity file.</p>
          <ul className="list-disc ml-4 space-y-1">
            <li>Do NOT send your passphrase to anyone.</li>
            <li>Do NOT post it on X or GitHub.</li>
          </ul>
        </div>
      </div>
      <div className="space-y-4">
        <div>
          <label className="text-gray-300 text-sm block mb-1">Passphrase</label>
          <input type="password" placeholder="••••••••••••••••" className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white" 
            onChange={(e) => setData({...data, passphrase: e.target.value})} />
        </div>
      </div>
      <button onClick={() => simulateProcess(1000, nextStep)} className="w-full bg-blue-600 text-white px-4 py-3 rounded-lg font-bold flex justify-center items-center gap-2">
        {loading ? "Generating..." : <><Key className="w-5 h-5"/> Create My DID</>}
      </button>
    </div>
  );

  const Step6ShowDID = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white">Your Technocore DID</h2>
      <div className="bg-gray-900 border border-gray-700 p-4 rounded-lg">
        <p className="font-mono text-green-400 break-all text-sm">{data.did}</p>
        <button onClick={() => copyToClipboard(data.did)} className="mt-3 flex items-center gap-2 text-sm text-gray-300 hover:text-white">
          {data.copied ? <Check className="w-4 h-4 text-green-500"/> : <Copy className="w-4 h-4"/>} 
          {data.copied ? 'Copied!' : 'Copy DID'}
        </button>
      </div>
      <p className="text-sm text-gray-300">
        Your DID is your <strong>public</strong> identity. It is safe to publish. <br/>
        Your <code className="bg-gray-800 px-1 rounded">identity.pem</code> file and passphrase must remain private.
      </p>
      
      <div className="bg-red-900/20 border border-red-500/50 p-4 rounded-lg mt-4">
        <h3 className="font-bold text-red-400 flex items-center gap-2 mb-2"><ShieldAlert className="w-5 h-5"/> BACKUP REQUIRED</h3>
        <p className="text-sm text-red-200">
          Anyone who obtains your identity.pem and passphrase can use your identity.
        </p>
      </div>
      <button onClick={nextStep} className="w-full bg-gray-700 hover:bg-gray-600 text-white px-4 py-3 rounded-lg font-bold">
        Save Backup & Continue
      </button>
    </div>
  );

  const Step7Test = () => {
    useEffect(() => { simulateProcess(2000, nextStep) }, []);
    return (
      <div className="space-y-6 text-center">
        <h2 className="text-2xl font-bold text-white">Testing Connection</h2>
        <div className="bg-gray-900 p-6 rounded-lg text-left font-mono text-sm space-y-2">
          <p className="text-gray-400">{">"} python technocore_agent.py read lobby</p>
          {loading ? (
             <p className="text-yellow-400 animate-pulse">Connecting to network...</p>
          ) : (
            <>
              <p className="text-green-400">✅ Connected</p>
              <p className="text-green-400">✅ Lobby readable</p>
              <p className="text-green-400">✅ Messages received</p>
              <p className="text-green-400">✅ DID environment working</p>
            </>
          )}
        </div>
      </div>
    );
  };

  const Step8Contribute = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white">Make a Contribution</h2>
      <p className="text-gray-300">Choose what you created and provide the URL.</p>
      
      <select className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white">
        <option>Useful tool</option>
        <option>Guide / Tutorial</option>
        <option>Code / Script</option>
        <option>Other</option>
      </select>

      <div>
        <label className="text-gray-300 text-sm block mb-1">Contribution URL</label>
        <input type="text" defaultValue={data.repoUrl} className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white font-mono text-sm" />
      </div>

      <button onClick={() => simulateProcess(1500, nextStep)} className="w-full bg-blue-600 text-white px-4 py-3 rounded-lg font-bold">
        {loading ? "Detecting Git Status..." : "Scan Repository"}
      </button>
    </div>
  );

  const Step9Proof = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white">Proof Generated</h2>
      <div className="bg-gray-900 border border-gray-700 p-4 rounded-lg font-mono text-sm text-green-300 overflow-x-auto">
        <pre>{JSON.stringify({
          artifact_url: data.repoUrl,
          commit: data.commit,
          did: data.did,
          schema: "technocore-contribution-proof-v1",
          signature: "3045022100e...a9f" 
        }, null, 2)}</pre>
      </div>
      <div className="flex gap-2">
        <CheckCircle2 className="text-green-500 w-5 h-5"/>
        <span className="text-gray-300 text-sm">Commit {data.commit.substring(0,7)} detected</span>
      </div>
      <button onClick={() => simulateProcess(1000, nextStep)} className="w-full bg-blue-600 text-white px-4 py-3 rounded-lg font-bold">
        {loading ? "Verifying..." : "Verify Contribution"}
      </button>
    </div>
  );

  const Step10Dashboard = () => {
    const tweetText = encodeURIComponent(`Just completed my Technocore contributor setup ✅\n\nDID: ${data.did}\nContribution: ${data.repoUrl}\n\nBuilding the Technocore ecosystem. ⚡`);
    return (
      <div className="space-y-6">
        <div className="text-center">
          <div className="w-16 h-16 bg-green-500/20 text-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckCircle2 className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-bold text-white">You're ready!</h2>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-900 p-4 rounded-lg border border-gray-800">
            <h3 className="text-gray-400 font-bold mb-2 text-sm uppercase tracking-wider">Identity & Network</h3>
            <ul className="text-sm space-y-1 text-gray-300">
              <li className="flex gap-2"><CheckCircle2 className="w-4 h-4 text-green-500"/> DID created</li>
              <li className="flex gap-2"><CheckCircle2 className="w-4 h-4 text-green-500"/> Identity backed up</li>
              <li className="flex gap-2"><CheckCircle2 className="w-4 h-4 text-green-500"/> Lobby tested</li>
            </ul>
          </div>
          <div className="bg-gray-900 p-4 rounded-lg border border-gray-800">
            <h3 className="text-gray-400 font-bold mb-2 text-sm uppercase tracking-wider">Contribution</h3>
            <ul className="text-sm space-y-1 text-gray-300">
              <li className="flex gap-2"><CheckCircle2 className="w-4 h-4 text-green-500"/> Artifact registered</li>
              <li className="flex gap-2"><CheckCircle2 className="w-4 h-4 text-green-500"/> Commit detected</li>
              <li className="flex gap-2"><CheckCircle2 className="w-4 h-4 text-green-500"/> Proof verified</li>
            </ul>
          </div>
        </div>

        <a href={`https://twitter.com/intent/tweet?text=${tweetText}`} target="_blank" rel="noreferrer" 
           className="w-full bg-black border border-gray-700 hover:bg-gray-900 text-white px-4 py-3 rounded-lg font-bold flex justify-center items-center gap-2 transition">
          <Twitter className="w-5 h-5"/> Share on X
        </a>
      </div>
    );
  };

  const renderStep = () => {
    switch(step) {
      case 1: return <Step1Welcome />;
      case 2: return <Step2SysCheck />;
      case 3: return <Step3Download />;
      case 4: return <Step4Env />;
      case 5: return <Step5CreateDID />;
      case 6: return <Step6ShowDID />;
      case 7: return <Step7Test />;
      case 8: return <Step8Contribute />;
      case 9: return <Step9Proof />;
      case 10: return <Step10Dashboard />;
      default: return <Step1Welcome />;
    }
  };

  return (
    <div className="min-h-screen bg-black text-gray-100 flex items-center justify-center p-4 font-sans">
      <div className="max-w-md w-full">
        <div className="mb-8 flex justify-between items-center px-2">
           <span className="text-xs font-bold text-gray-500 tracking-widest uppercase">Technocore Setup</span>
           <span className="text-xs font-bold text-blue-500">{step} / 10</span>
        </div>
        <div className="h-1 w-full bg-gray-900 rounded-full mb-8 overflow-hidden">
           <div className="h-full bg-blue-600 transition-all duration-500" style={{width: `${(step / 10) * 100}%`}}></div>
        </div>
        
        <div className="bg-gray-950 border border-gray-800 shadow-2xl rounded-2xl p-8">
          {renderStep()}
        </div>

        <div className="mt-8 text-center flex items-center justify-center gap-2 text-xs text-gray-600">
          <ShieldAlert className="w-4 h-4" />
          <span>Local execution only. Keys never leave your device.</span>
        </div>
      </div>
    </div>
  );
}
