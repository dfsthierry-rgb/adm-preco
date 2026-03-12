import sys

filepath = 'index.html'
with open(filepath, 'rb') as f:
    content = f.read()

# 1. Update saveToCloud
old_save = b'''const saveToCloud = async (newParams, newConfig) => {
  const config = newConfig || s;
  const params = newParams || a;
  if (!config.syncUrl) return;
  try {
    await fetch(config.syncUrl + (config.syncUrl.includes("?") ? "&" : "?") + "action=saveConfig", {
      method: "POST",
      mode: "no-cors",
      body: JSON.stringify({ params, config })
    });
  } catch (e) {
    console.error("Erro ao salvar na nuvem:", e);
  }
};'''

new_save = b'''const saveToCloud = async (newParams, newConfig, newLastPubs) => {
  const config = newConfig || s;
  const params = newParams || a;
  const lastPubs = newLastPubs || H;
  if (!config.syncUrl) return;
  try {
    const simple = localStorage.getItem("centralMeshSimple");
    const compare = localStorage.getItem("centralMeshCompare");
    await fetch(config.syncUrl + (config.syncUrl.includes("?") ? "&" : "?") + "action=saveConfig", {
      method: "POST",
      mode: "no-cors",
      body: JSON.stringify({ params, config, lastPubs, simple, compare })
    });
  } catch (e) {
    console.error("Erro ao salvar na nuvem:", e);
  }
};'''

if old_save in content:
    content = content.replace(old_save, new_save)
    print('saveToCloud updated')
else:
    print('old_save not found')

# 2. Update loadFromCloud
old_load = b'''const loadFromCloud = async (url) => {
  const targetUrl = url || s.syncUrl;
  if (!targetUrl) return;
  try {
    const response = await fetch(targetUrl + (targetUrl.includes("?") ? "&" : "?") + "action=loadConfig");
    const data = await response.json();
    if (data.params) {
      i(data.params);
      localStorage.setItem("centralMeshParams", JSON.stringify(data.params));
    }
    if (data.config) {
      A(data.config);
      localStorage.setItem("centralMeshConfig", JSON.stringify(data.config));
    }
  } catch (e) {
    console.error("Erro ao carregar da nuvem:", e);
  }
};'''

new_load = b'''const loadFromCloud = async (url) => {
  const targetUrl = url || s.syncUrl;
  if (!targetUrl) return;
  try {
    const response = await fetch(targetUrl + (targetUrl.includes("?") ? "&" : "?") + "action=loadConfig");
    const data = await response.json();
    if (data.params) {
      i(data.params);
      localStorage.setItem("centralMeshParams", JSON.stringify(data.params));
    }
    if (data.config) {
      A(data.config);
      localStorage.setItem("centralMeshConfig", JSON.stringify(data.config));
    }
    if (data.lastPubs) {
      L(data.lastPubs);
      localStorage.setItem("centralMeshLastPubs", JSON.stringify(data.lastPubs));
    }
    if (data.simple) {
      localStorage.setItem("centralMeshSimple", data.simple);
      O(!0);
    }
    if (data.compare) {
      localStorage.setItem("centralMeshCompare", data.compare);
      Y(!0);
    }
  } catch (e) {
    console.error("Erro ao carregar da nuvem:", e);
  }
};'''

if old_load in content:
    content = content.replace(old_load, new_load)
    print('loadFromCloud updated')
else:
    print('old_load not found')

# 3. Update V
old_V = b'L(se),localStorage.setItem("centralMeshLastPubs",JSON.stringify(se)),B(Ee=>({...Ee,confirmParams:!1,publish:!0}))'
new_V = b'L(se),localStorage.setItem("centralMeshLastPubs",JSON.stringify(se)),saveToCloud(null,null,se),B(Ee=>({...Ee,confirmParams:!1,publish:!0}))'

if old_V in content:
    content = content.replace(old_V, new_V)
    print('V updated')
else:
    print('old_V not found')

# 4. Update useEffect analysis
old_effect = b'localStorage.setItem(z,JSON.stringify({data:l,timestamp:new Date().toISOString(),itemCount:l.length}))}'
new_effect = b'localStorage.setItem(z,JSON.stringify({data:l,timestamp:new Date().toISOString(),itemCount:l.length})),saveToCloud()}'

if old_effect in content:
    content = content.replace(old_effect, new_effect)
    print('useEffect analysis updated')
else:
    print('old_effect not found')

with open(filepath, 'wb') as f:
    f.write(content)
