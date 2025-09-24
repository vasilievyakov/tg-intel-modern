"use client";

import * as React from "react";
import {
  ColumnDef,
  ColumnFiltersState,
  SortingState,
  VisibilityState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
  getFacetedRowModel,
  getFacetedUniqueValues,
} from "@tanstack/react-table";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { 
  Eye, 
  RefreshCw, 
  MessageCircle, 
  Heart, 
  Search, 
  Filter, 
  ChevronDown, 
  ChevronUp,
  ArrowUpDown,
  MoreHorizontal,
  X
} from "lucide-react";

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
  searchPlaceholder?: string;
  showFilters?: boolean;
  meta?: any;
}

export function DataTable<TData, TValue>({ 
  columns, 
  data, 
  searchPlaceholder = "Поиск по всем полям...",
  showFilters = true,
  meta
}: DataTableProps<TData, TValue>) {
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([]);
  const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({});
  const [globalFilter, setGlobalFilter] = React.useState("");
  const [showColumnFilters, setShowColumnFilters] = React.useState(false);

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    onSortingChange: setSorting,
    getSortedRowModel: getSortedRowModel(),
    onColumnFiltersChange: setColumnFilters,
    getFilteredRowModel: getFilteredRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    onGlobalFilterChange: setGlobalFilter,
    getFacetedRowModel: getFacetedRowModel(),
    getFacetedUniqueValues: getFacetedUniqueValues(),
    state: { 
      sorting, 
      columnFilters, 
      columnVisibility, 
      globalFilter 
    },
    initialState: {
      pagination: {
        pageSize: 20,
      },
    },
    meta,
  });

  return (
    <div className="space-y-4">
      {/* Search and Filters */}
      <Card>
        <CardHeader className="pb-4">
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg">Фильтры и поиск</CardTitle>
            {showFilters && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowColumnFilters(!showColumnFilters)}
              >
                <Filter className="w-4 h-4 mr-2" />
                {showColumnFilters ? "Скрыть фильтры" : "Показать фильтры"}
                {showColumnFilters ? <ChevronUp className="w-4 h-4 ml-2" /> : <ChevronDown className="w-4 h-4 ml-2" />}
              </Button>
            )}
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Global Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
            <Input
              placeholder={searchPlaceholder}
              value={globalFilter}
              onChange={(e) => setGlobalFilter(e.target.value)}
              className="pl-10"
            />
            {globalFilter && (
              <Button
                variant="ghost"
                size="sm"
                className="absolute right-2 top-1/2 transform -translate-y-1/2 h-6 w-6 p-0"
                onClick={() => setGlobalFilter("")}
              >
                <X className="w-4 h-4" />
              </Button>
            )}
          </div>

          {/* Column Filters */}
          {showFilters && showColumnFilters && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pt-4 border-t">
              {table.getHeaderGroups()[0]?.headers
                .filter((header) => header.column.getCanFilter())
                .map((header) => (
                  <div key={header.id} className="space-y-2">
                    <label className="text-sm font-medium text-muted-foreground">
                      {header.column.columnDef.header as string}
                    </label>
                    <Input
                      placeholder={`Фильтр по ${header.column.columnDef.header}`}
                      value={(header.column.getFilterValue() as string) ?? ""}
                      onChange={(e) => header.column.setFilterValue(e.target.value)}
                      className="h-8"
                    />
                  </div>
                ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                {table.getHeaderGroups().map((headerGroup) => (
                  <TableRow key={headerGroup.id}>
                    {headerGroup.headers.map((header) => (
                      <TableHead key={header.id} className="px-4 py-3">
                        {header.isPlaceholder ? null : (
                          <div className="flex items-center space-x-2">
                            <button
                              className="flex items-center space-x-1 hover:text-foreground"
                              onClick={header.column.getToggleSortingHandler()}
                            >
                              <span>{flexRender(header.column.columnDef.header, header.getContext())}</span>
                              {header.column.getCanSort() && (
                                <ArrowUpDown className="w-4 h-4" />
                              )}
                            </button>
                          </div>
                        )}
                      </TableHead>
                    ))}
                  </TableRow>
                ))}
              </TableHeader>
              <TableBody>
                {table.getRowModel().rows?.length ? (
                  table.getRowModel().rows.map((row) => (
                    <TableRow key={row.id} className="hover:bg-muted/50">
                      {row.getVisibleCells().map((cell) => (
                        <TableCell key={cell.id} className="px-4 py-3">
                          {flexRender(cell.column.columnDef.cell, cell.getContext())}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={columns.length} className="h-24 text-center">
                      <div className="flex flex-col items-center justify-center space-y-2">
                        <div className="text-4xl">📝</div>
                        <p className="text-muted-foreground">Постов не найдено</p>
                        {globalFilter && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setGlobalFilter("")}
                          >
                            Очистить поиск
                          </Button>
                        )}
                      </div>
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      {/* Pagination */}
      <Card>
        <CardContent className="py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <p className="text-sm text-muted-foreground">
                Показано {table.getFilteredRowModel().rows.length} из {data.length} записей
              </p>
              {globalFilter && (
                <Badge variant="secondary">
                  Фильтр: "{globalFilter}"
                </Badge>
              )}
            </div>
            
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => table.previousPage()}
                disabled={!table.getCanPreviousPage()}
              >
                ← Предыдущая
              </Button>
              
              <div className="flex items-center space-x-1">
                <span className="text-sm text-muted-foreground">Страница</span>
                <Badge variant="secondary" className="px-3 py-1">
                  {table.getState().pagination.pageIndex + 1} из {table.getPageCount()}
                </Badge>
              </div>
              
              <Button
                variant="outline"
                size="sm"
                onClick={() => table.nextPage()}
                disabled={!table.getCanNextPage()}
              >
                Следующая →
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}


