"use client";

import { ColumnDef } from "@tanstack/react-table";
import { Button } from "../ui/button";
import { Badge } from "../ui/badge";
import { Card, CardContent } from "../ui/card";
import { 
  Eye, 
  RefreshCw, 
  Trash2, 
  ExternalLink,
  Calendar,
  Hash,
  Globe,
  Activity
} from "lucide-react";
import Link from "next/link";

export type Channel = {
  id: number;
  tg_url: string;
  title?: string | null;
  status: string;
  created_at: string;
};

export const channelsColumns: ColumnDef<Channel>[] = [
  {
    accessorKey: "id",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 lg:px-3"
        >
          <Hash className="mr-2 h-4 w-4" />
          ID
        </Button>
      );
    },
    cell: ({ row }) => {
      return (
        <div className="flex items-center space-x-2">
          <Badge variant="outline" className="font-mono">
            #{row.getValue("id")}
          </Badge>
        </div>
      );
    },
    enableSorting: true,
    enableHiding: false,
  },
  {
    accessorKey: "title",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 lg:px-3"
        >
          <Globe className="mr-2 h-4 w-4" />
          Название канала
        </Button>
      );
    },
    cell: ({ row }) => {
      const title = row.getValue("title") as string | null;
      const url = row.getValue("tg_url") as string;
      return (
        <div className="max-w-xs">
          <div className="font-medium text-foreground">
            {title || url}
          </div>
          <div className="text-sm text-muted-foreground truncate">
            {url}
          </div>
        </div>
      );
    },
    enableSorting: true,
  },
  {
    accessorKey: "status",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 lg:px-3"
        >
          <Activity className="mr-2 h-4 w-4" />
          Статус
        </Button>
      );
    },
    cell: ({ row }) => {
      const status = row.getValue("status") as string;
      return (
        <div className="flex items-center space-x-2">
          <div className={`w-2 h-2 rounded-full ${
            status === 'active' ? 'bg-green-500' : 
            status === 'paused' ? 'bg-yellow-500' : 'bg-red-500'
          }`}></div>
          <Badge 
            variant={status === 'active' ? 'default' : status === 'paused' ? 'secondary' : 'destructive'}
            className="text-xs"
          >
            {status}
          </Badge>
        </div>
      );
    },
    enableSorting: true,
  },
  {
    accessorKey: "created_at",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="h-8 px-2 lg:px-3"
        >
          <Calendar className="mr-2 h-4 w-4" />
          Дата добавления
        </Button>
      );
    },
    cell: ({ row }) => {
      const date = row.getValue("created_at") as string;
      return (
        <div className="text-sm">
          <div className="font-medium">
            {new Date(date).toLocaleDateString('ru-RU')}
          </div>
          <div className="text-muted-foreground">
            {new Date(date).toLocaleTimeString('ru-RU')}
          </div>
        </div>
      );
    },
    enableSorting: true,
  },
  {
    id: "actions",
    header: "Действия",
    cell: ({ row, table }) => {
      const channel = row.original;
      const meta = table.options.meta as any;
      
      return (
        <div className="flex items-center space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => meta?.onRefresh?.(channel.id)}
            className="h-8 px-2"
          >
            <RefreshCw className="w-4 h-4" />
          </Button>
          
          <Button variant="outline" size="sm" asChild className="h-8 px-2">
            <Link href={`/channels/${channel.id}`}>
              <Eye className="w-4 h-4" />
            </Link>
          </Button>
          
          <Button
            variant="outline"
            size="sm"
            onClick={() => meta?.onDelete?.(channel.id)}
            className="h-8 px-2 text-destructive hover:text-destructive"
          >
            <Trash2 className="w-4 h-4" />
          </Button>
          
          <Button
            variant="outline"
            size="sm"
            asChild
            className="h-8 px-2"
          >
            <a 
              href={channel.tg_url} 
              target="_blank" 
              rel="noopener noreferrer"
            >
              <ExternalLink className="w-4 h-4" />
            </a>
          </Button>
        </div>
      );
    },
    enableSorting: false,
    enableHiding: false,
  },
];
