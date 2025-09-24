import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/router";
import { DataTable } from "../../components/data-table";
import { columns, ChannelPost } from "../../components/channels/columns";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Search, RefreshCw, CheckCircle, XCircle, Clock } from "lucide-react";

type Post = {
  id: number;
  channel_id: number;
  tg_message_id: number;
  posted_at?: string | null;
  text?: string | null;
  views?: number | null;
  forwards?: number | null;
  replies?: number | null;
  reactions?: number | null;
};

type PostsPage = {
  items: Post[];
  page: number;
  page_size: number;
  total: number;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function Channel() {
  const router = useRouter();
  const id = useMemo(() => (router.query.id ? Number(router.query.id) : undefined), [router.query.id]);
  const [q, setQ] = useState("");
  const [page, setPage] = useState(1);
  const [data, setData] = useState<PostsPage | null>(null);
  const [job, setJob] = useState<any | null>(null);
  const [summaries, setSummaries] = useState<Record<number, string>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function fetchPosts() {
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      const url = new URL(`${API_BASE}/api/channels/${id}/posts`);
      if (q) url.searchParams.set("query", q);
      url.searchParams.set("page", String(page));
      url.searchParams.set("page_size", "20");
      const res = await fetch(url.toString());
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = (await res.json()) as PostsPage;
      setData(json);
    } catch (e: any) {
      setError(e?.message || "Failed to load posts");
    } finally {
      setLoading(false);
    }
  }

  async function fetchJob() {
    if (!id) return;
    try {
      const res = await fetch(`${API_BASE}/api/channels/${id}/jobs/latest`);
      if (res.ok) {
        const j = await res.json();
        setJob(j);
      }
    } catch {}
  }

  async function doSummarize(postId: number) {
    try {
      const res = await fetch(`${API_BASE}/api/posts/${postId}/summarize`, { method: "POST" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = await res.json();
      setSummaries((prev) => ({ ...prev, [postId]: json.summary as string }));
    } catch (e) {
      // ignore for now
    }
  }

  useEffect(() => {
    fetchPosts();
    fetchJob();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id, q, page]);

  // Poll job status for a short period when there is no data
  useEffect(() => {
    if (!id) return;
    const t = setInterval(() => {
      fetchJob();
      fetchPosts();
    }, 5000);
    return () => clearInterval(t);
  }, [id]);

  return (
    <div className="min-h-screen bg-background">
      <main className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-3xl">📺 Канал #{id}</CardTitle>
                <CardDescription>
                  Просмотр постов и статистики канала
                </CardDescription>
              </div>
              <Button variant="outline" onClick={() => router.back()}>
                <ArrowLeft className="w-4 h-4 mr-2" />
                Назад
              </Button>
            </div>
          </CardHeader>
        </Card>

        {/* Channel Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Статус</p>
                  <p className="text-2xl font-bold">Активен</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center space-x-2">
                <RefreshCw className="w-5 h-5 text-blue-500" />
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Последнее обновление</p>
                  <p className="text-2xl font-bold">
                    {job?.status === 'completed' ? '✅' : job?.status === 'failed' ? '❌' : '⏳'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center space-x-2">
                <CheckCircle className="w-5 h-5 text-green-500" />
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Всего постов</p>
                  <p className="text-2xl font-bold">{data?.total || 0}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Job Status */}
        {job && (
          <Card className="mb-6">
            <CardContent className="pt-6">
              <div className="flex items-center gap-3">
                <div className={`w-3 h-3 rounded-full ${
                  job.status === 'completed' ? 'bg-green-500' : 
                  job.status === 'failed' ? 'bg-red-500' : 'bg-yellow-500'
                }`}></div>
                <div className="flex-1">
                  <p className="text-sm font-medium">
                    Статус обновления: {job.status || 'n/a'}
                  </p>
                  {job.error && (
                    <p className="text-sm text-destructive mt-1">
                      Ошибка: {job.error}
                    </p>
                  )}
                  {job.stats?.inserted && (
                    <p className="text-sm text-green-600 mt-1">
                      ✅ Добавлено постов: {job.stats.inserted}
                    </p>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Error */}
        {error && (
          <Card className="mb-6 border-destructive">
            <CardContent className="pt-6">
              <p className="text-destructive">{error}</p>
            </CardContent>
          </Card>
        )}

        {/* Posts Table */}
        {loading ? (
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
                <span className="ml-3 text-muted-foreground">Загрузка постов...</span>
              </div>
            </CardContent>
          </Card>
        ) : !data || data.items.length === 0 ? (
          <Card>
            <CardContent className="pt-6">
              <div className="text-center py-12">
                <div className="text-6xl mb-4">📝</div>
                <p className="text-muted-foreground text-lg">Постов пока нет</p>
                <p className="text-muted-foreground/70 text-sm mt-2">
                  {q ? 'Попробуйте изменить поисковый запрос' : 'Канал еще не обновлялся или посты не найдены'}
                </p>
              </div>
            </CardContent>
          </Card>
        ) : (
          <DataTable 
            columns={columns} 
            data={data.items as unknown as ChannelPost[]}
            searchPlaceholder="Поиск по постам, тексту, дате..."
            showFilters={true}
          />
        )}
      </main>
    </div>
  );
}


