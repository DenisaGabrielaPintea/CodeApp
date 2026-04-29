from flask import Flask, request, render_template_string
import ipaddress

app = Flask(__name__)


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Subnet Mask Calculator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-[#0f172a] text-slate-200 min-h-screen flex items-center justify-center p-4">
    <div class="max-w-3xl w-full bg-[#1e293b] rounded-3xl shadow-2xl overflow-hidden border border-slate-700/50">
        <div class="bg-gradient-to-br from-indigo-500 to-purple-600 p-10 text-center">
            <h1 class="text-4xl font-extrabold text-white tracking-tight">Subnet Mask Calculator</h1>
            <p class="text-indigo-100 mt-2 text-lg opacity-90">Professional IPv4 Networking Utility</p>
        </div>
        <div class="p-8 md:p-12">
            <form method="POST" class="space-y-6 mb-10">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="md:col-span-2">
                        <label class="block text-sm font-semibold mb-2 text-slate-400 uppercase tracking-wider">IP Address</label>
                        <input type="text" name="ip" placeholder="e.g. 192.168.1.1" required
                            class="w-full bg-[#0f172a] border border-slate-600 rounded-xl p-4 focus:ring-2 focus:ring-indigo-500 outline-none transition text-white placeholder-slate-500">
                    </div>
                    <div>
                        <label class="block text-sm font-semibold mb-2 text-slate-400 uppercase tracking-wider">CIDR Mask</label>
                        <input type="number" name="mask" placeholder="24" min="0" max="32" required
                            class="w-full bg-[#0f172a] border border-slate-600 rounded-xl p-4 focus:ring-2 focus:ring-indigo-500 outline-none transition text-white placeholder-slate-500">
                    </div>
                </div>
                <button type="submit" class="w-full bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-4 rounded-xl transition duration-300 transform hover:-translate-y-1 shadow-lg shadow-indigo-500/20">
                    CALCULATE NETWORK DETAILS
                </button>
            </form>

            {% if error %}
            <div class="bg-rose-500/10 border border-rose-500/50 text-rose-400 p-4 rounded-xl mb-8 flex items-center space-x-3">
                <span>{{ error }}</span>
            </div>
            {% endif %}

            {% if result %}
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-slate-800/40 p-5 rounded-2xl border border-slate-700/50 hover:border-indigo-500/50 transition">
                    <span class="text-xs text-indigo-400 font-bold uppercase tracking-widest">Network Address</span>
                    <p class="text-xl font-mono mt-1 text-white">{{ result.network_address }}{{ result.cidr }}</p>
                </div>
                <div class="bg-slate-800/40 p-5 rounded-2xl border border-slate-700/50 hover:border-indigo-500/50 transition">
                    <span class="text-xs text-indigo-400 font-bold uppercase tracking-widest">Broadcast Address</span>
                    <p class="text-xl font-mono mt-1 text-white">{{ result.broadcast_address }}</p>
                </div>
                <div class="bg-slate-800/40 p-5 rounded-2xl border border-slate-700/50 hover:border-indigo-500/50 transition">
                    <span class="text-xs text-indigo-400 font-bold uppercase tracking-widest">Subnet Mask</span>
                    <p class="text-xl font-mono mt-1 text-white">{{ result.netmask }}</p>
                </div>
                <div class="md:col-span-3 bg-indigo-500/5 p-6 rounded-2xl border border-indigo-500/30 mt-2">
                    <div class="flex justify-between items-center">
                        <div>
                            <span class="text-xs text-indigo-400 font-bold uppercase tracking-widest">Usable Hosts</span>
                            <p class="text-4xl font-black text-white mt-1">{{ result.num_hosts }}</p>
                        </div>
                        <div class="text-right">
                            <span class="text-xs text-slate-500 font-bold uppercase tracking-widest">Host Range</span>
                            <p class="text-sm font-mono text-slate-300 mt-1">{{ result.host_range }}</p>
                        </div>
                    </div>
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        try:
            ip_input = request.form.get('ip')
            mask_input = request.form.get('mask')
            network = ipaddress.IPv4Interface(f"{ip_input}/{mask_input}")
            net_obj = network.network
            result = {
                "network_address": str(net_obj.network_address),
                "broadcast_address": str(net_obj.broadcast_address),
                "netmask": str(net_obj.netmask),
                "num_hosts": net_obj.num_addresses - 2 if net_obj.num_addresses > 2 else 0,
                "host_range": f"{net_obj.network_address + 1} - {net_obj.broadcast_address - 1}" if net_obj.num_addresses > 2 else "N/A",
                "cidr": f"/{mask_input}"
            }
        except Exception:
            error = "Invalid input! Please check the IP and Subnet Mask."

    return render_template_string(HTML_TEMPLATE, result=result, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)