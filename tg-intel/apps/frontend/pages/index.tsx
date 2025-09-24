import { useEffect, useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { DataTable } from "@/components/data-table";
import { channelsColumns, Channel } from "@/components/channels/channels-columns";
import { Plus, Activity, Globe, Calendar } from "lucide-react";

// Channel type is now imported from channels-columns.tsx

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function Home() {
  const [channels, setChannels] = useState<Channel[]>([]);
  const [loading, setLoading] = useState(false);
  const [url, setUrl] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function fetchChannels() {
    setLoading(true);
    setError(null);
    try {
      console.log("Fetching channels from:", `${API_BASE}/api/channels`);
      const res = await fetch(`${API_BASE}/api/channels`);
      const data = await res.json();
      console.log("Channels data:", data);
      setChannels(Array.isArray(data) ? data : (data.channels || []));
    } catch (e: any) {
      console.error("Error fetching channels:", e);
      setError(e?.message || "Failed to load channels");
    } finally {
      setLoading(false);
    }
  }

  async function addChannel(e: React.FormEvent) {
    e.preventDefault();
    console.log("Adding channel:", url);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/api/channels`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tg_url: url }),
      });
      console.log("Response status:", res.status);
      if (!res.ok) {
        let details = "";
        try { details = await res.text(); } catch {}
        throw new Error(`HTTP ${res.status}${details ? ` — ${details}` : ""}`);
      }
      const newChannel = await res.json();
      console.log("New channel:", newChannel);
      // Обновляем список каналов с сервера вместо локального добавления
      await fetchChannels();
      setUrl("");
    } catch (e: any) {
      console.error("Error adding channel:", e);
      setError(e?.message || "Failed to add channel");
    }
  }

  useEffect(() => {
    fetchChannels();
    const t = setInterval(fetchChannels, 5000);
    return () => clearInterval(t);
  }, []);

  async function forceFetch(id: number) {
    try {
      await fetch(`${API_BASE}/api/channels/${id}/fetch`, { method: "POST" });
      await fetchChannels();
    } catch {}
  }

  async function deleteChannel(id: number) {
    try {
      await fetch(`${API_BASE}/api/channels/${id}`, { method: "DELETE" });
      await fetchChannels();
    } catch (e: any) {
      setError(e?.message || "Failed to delete channel");
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            📱 tg-intel
          </h1>
          <p className="text-muted-foreground text-lg">
            Мониторинг и анализ Telegram каналов
          </p>
        </div>

        {/* Add Channel Form */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Добавить новый канал</CardTitle>
            <CardDescription>
              Введите ссылку на Telegram канал для начала мониторинга
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={addChannel} className="flex gap-3">
              <Input
                placeholder="https://t.me/durov или @durov"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="flex-1"
              />
              <Button type="submit" disabled={!url}>
                <Plus className="w-4 h-4 mr-2" />
                Добавить
              </Button>
            </form>
            {error && (
              <div className="mt-3 p-3 bg-destructive/10 border border-destructive/20 rounded-lg">
                <p className="text-destructive text-sm">{error}</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Channels Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center space-x-2">
                <Globe className="w-5 h-5 text-blue-500" />
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Всего каналов</p>
                  <p className="text-2xl font-bold">{channels.length}</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center space-x-2">
                <Activity className="w-5 h-5 text-green-500" />
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Активных</p>
                  <p className="text-2xl font-bold">
                    {channels.filter(c => c.status === 'active').length}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center space-x-2">
                <Calendar className="w-5 h-5 text-purple-500" />
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Добавлено сегодня</p>
                  <p className="text-2xl font-bold">
                    {channels.filter(c => {
                      const today = new Date();
                      const created = new Date(c.created_at);
                      return created.toDateString() === today.toDateString();
                    }).length}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Channels Table */}
        {loading ? (
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
                <span className="ml-3 text-muted-foreground">Загрузка...</span>
              </div>
            </CardContent>
          </Card>
        ) : channels.length === 0 ? (
          <Card>
            <CardContent className="pt-6">
              <div className="text-center py-12">
                <div className="text-6xl mb-4">📭</div>
                <p className="text-muted-foreground text-lg">Пока нет каналов</p>
                <p className="text-muted-foreground/70 text-sm mt-2">
                  Добавьте первый канал выше, чтобы начать мониторинг
                </p>
              </div>
            </CardContent>
          </Card>
        ) : (
          <DataTable 
            columns={channelsColumns} 
            data={channels}
            searchPlaceholder="Поиск по каналам, названию, URL..."
            showFilters={true}
            meta={{
              onRefresh: forceFetch,
              onDelete: deleteChannel
            }}
          />
        )}
      </main>
    </div>
  );
}


