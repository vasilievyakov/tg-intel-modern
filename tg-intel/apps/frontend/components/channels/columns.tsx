"use client";

import { ColumnDef } from "@tanstack/react-table";
import { Button } from "../ui/button";
import { Badge } from "../ui/badge";
import { Card, CardContent } from "../ui/card";
import { 
  Eye, 
  RefreshCw, 
  MessageCircle, 
  Heart, 
  Calendar,
  Hash,
  FileText,
  TrendingUp
} from "lucide-react";

export type ChannelPost = {
  id: number;
  tg_message_id: number;
  posted_at?: string | null;
  text?: string | null;
  views?: number | null;
  forwards?: number | null;
  replies?: number | null;
  reactions?: number | null;
};

export const columns: ColumnDef<ChannelPost>[] = [
  {
    accessorKey: "tg_message_id",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 lg:px-3"
        >
          <Hash className="mr-2 h-4 w-4" />
          ID сообщения
        </Button>
      );
    },
    cell: ({ row }) => {
      return (
        <div className="flex items-center space-x-2">
          <Badge variant="outline" className="font-mono">
            #{row.getValue("tg_message_id")}
          </Badge>
        </div>
      );
    },
    enableSorting: true,
    enableHiding: false,
  },
  {
    accessorKey: "posted_at",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 lg:px-3"
        >
          <Calendar className="mr-2 h-4 w-4" />
          Дата публикации
        </Button>
      );
    },
    cell: ({ row }) => {
      const date = row.getValue("posted_at") as string | null;
      return (
        <div className="text-sm">
          {date ? (
            <div>
              <div className="font-medium">
                {new Date(date).toLocaleDateString('ru-RU')}
              </div>
              <div className="text-muted-foreground">
                {new Date(date).toLocaleTimeString('ru-RU')}
              </div>
            </div>
          ) : (
            <span className="text-muted-foreground italic">Не указано</span>
          )}
        </div>
      );
    },
    enableSorting: true,
  },
  {
    accessorKey: "text",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 lg:px-3"
        >
          <FileText className="mr-2 h-4 w-4" />
          Текст сообщения
        </Button>
      );
    },
    cell: ({ row }) => {
      const text = row.getValue("text") as string | null;
      return (
        <div className="max-w-xs">
          {text ? (
            <Card className="p-2">
              <CardContent className="p-0">
                <p className="text-sm line-clamp-3 whitespace-pre-wrap">
                  {text}
                </p>
              </CardContent>
            </Card>
          ) : (
            <span className="text-muted-foreground italic text-sm">(нет текста)</span>
          )}
        </div>
      );
    },
    enableSorting: true,
  },
  {
    accessorKey: "views",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 lg:px-3"
        >
          <Eye className="mr-2 h-4 w-4" />
          Просмотры
        </Button>
      );
    },
    cell: ({ row }) => {
      const views = row.getValue("views") as number | null;
      return (
        <div className="flex items-center space-x-1">
          <Eye className="h-4 w-4 text-muted-foreground" />
          <span className="font-medium">{views || 0}</span>
        </div>
      );
    },
    enableSorting: true,
  },
  {
    accessorKey: "forwards",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 lg:px-3"
        >
          <RefreshCw className="mr-2 h-4 w-4" />
          Пересылки
        </Button>
      );
    },
    cell: ({ row }) => {
      const forwards = row.getValue("forwards") as number | null;
      return (
        <div className="flex items-center space-x-1">
          <RefreshCw className="h-4 w-4 text-muted-foreground" />
          <span className="font-medium">{forwards || 0}</span>
        </div>
      );
    },
    enableSorting: true,
  },
  {
    accessorKey: "replies",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 lg:px-3"
        >
          <MessageCircle className="mr-2 h-4 w-4" />
          Ответы
        </Button>
      );
    },
    cell: ({ row }) => {
      const replies = row.getValue("replies") as number | null;
      return (
        <div className="flex items-center space-x-1">
          <MessageCircle className="h-4 w-4 text-muted-foreground" />
          <span className="font-medium">{replies || 0}</span>
        </div>
      );
    },
    enableSorting: true,
  },
  {
    accessorKey: "reactions",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 lg:px-3"
        >
          <Heart className="mr-2 h-4 w-4" />
          Реакции
        </Button>
      );
    },
    cell: ({ row }) => {
      const reactions = row.getValue("reactions") as number | null;
      return (
        <div className="flex items-center space-x-1">
          <Heart className="h-4 w-4 text-muted-foreground" />
          <span className="font-medium">{reactions || 0}</span>
        </div>
      );
    },
    enableSorting: true,
  },
  {
    id: "engagement",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 lg:px-3"
        >
          <TrendingUp className="mr-2 h-4 w-4" />
          Активность
        </Button>
      );
    },
    cell: ({ row }) => {
      const views = (row.getValue("views") as number) || 0;
      const forwards = (row.getValue("forwards") as number) || 0;
      const replies = (row.getValue("replies") as number) || 0;
      const reactions = (row.getValue("reactions") as number) || 0;
      
      const totalEngagement = views + forwards + replies + reactions;
      
      return (
        <div className="flex items-center space-x-2">
          <Badge 
            variant={totalEngagement > 1000 ? "default" : totalEngagement > 100 ? "secondary" : "outline"}
            className="font-medium"
          >
            {totalEngagement.toLocaleString()}
          </Badge>
        </div>
      );
    },
    enableSorting: true,
    sortingFn: (rowA, rowB) => {
      const getEngagement = (row: any) => {
        const views = (row.getValue("views") as number) || 0;
        const forwards = (row.getValue("forwards") as number) || 0;
        const replies = (row.getValue("replies") as number) || 0;
        const reactions = (row.getValue("reactions") as number) || 0;
        return views + forwards + replies + reactions;
      };
      
      return getEngagement(rowA) - getEngagement(rowB);
    },
  },
];


