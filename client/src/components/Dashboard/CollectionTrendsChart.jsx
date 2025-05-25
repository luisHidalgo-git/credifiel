import { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import {
  Paper,
  Typography,
  Box,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from "@mui/material";
import { motion } from "framer-motion";

const MotionPaper = motion(Paper);

const CollectionTrendsChart = ({ data }) => {
  const [selectedYear, setSelectedYear] = useState("all");
  const monthNames = [
    "Ene",
    "Feb",
    "Mar",
    "Abr",
    "May",
    "Jun",
    "Jul",
    "Ago",
    "Sep",
    "Oct",
    "Nov",
    "Dic",
  ];

  const formattedData = monthNames.map((month, idx) => ({
    month,
    "Cobrado 2022":
      data["2022"]?.find((d) => d.month === idx + 1)?.total_cobrado || 0,
    "Cobrado 2023":
      data["2023"]?.find((d) => d.month === idx + 1)?.total_cobrado || 0,
    "Cobrado 2024":
      data["2024"]?.find((d) => d.month === idx + 1)?.total_cobrado || 0,
    "Cobrado 2025":
      data["2025"]?.find((d) => d.month === idx + 1)?.total_cobrado || 0,
  }));

  const formatCurrency = (value) => {
    return new Intl.NumberFormat("es-MX", {
      style: "currency",
      currency: "MXN",
    }).format(value);
  };

  return (
    <MotionPaper
      elevation={3}
      sx={{
        p: 3,
        borderRadius: 2,
        background: "linear-gradient(145deg, #ffffff 0%, #f5f5f5 100%)",
      }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >
      <Box
        display="flex"
        justifyContent="space-between"
        alignItems="center"
        mb={2}
      >
        <Typography variant="h6" fontWeight="bold">
          Tendencias de Cobranza Mensual
        </Typography>
        <FormControl size="small" sx={{ minWidth: 120 }}>
          <InputLabel>Año</InputLabel>
          <Select
            value={selectedYear}
            label="Año"
            onChange={(e) => setSelectedYear(e.target.value)}
          >
            <MenuItem value="all">Todos</MenuItem>
            <MenuItem value="2022">2022</MenuItem>
            <MenuItem value="2023">2023</MenuItem>
            <MenuItem value="2024">2024</MenuItem>
            <MenuItem value="2025">2025</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={formattedData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
          <XAxis dataKey="month" stroke="#666" />
          <YAxis stroke="#666" tickFormatter={formatCurrency} />
          <Tooltip
            formatter={(value) => formatCurrency(value)}
            contentStyle={{
              backgroundColor: "rgba(255, 255, 255, 0.9)",
              border: "none",
              borderRadius: "8px",
              boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
            }}
          />
          <Legend />
          {(selectedYear === "all" || selectedYear === "2022") && (
            <Bar dataKey="Cobrado 2022" fill="#8884d8" radius={[4, 4, 0, 0]} />
          )}
          {(selectedYear === "all" || selectedYear === "2023") && (
            <Bar dataKey="Cobrado 2023" fill="#82ca9d" radius={[4, 4, 0, 0]} />
          )}
          {(selectedYear === "all" || selectedYear === "2024") && (
            <Bar dataKey="Cobrado 2024" fill="#ffc658" radius={[4, 4, 0, 0]} />
          )}
          {(selectedYear === "all" || selectedYear === "2025") && (
            <Bar dataKey="Cobrado 2025" fill="#ff7300" radius={[4, 4, 0, 0]} />
          )}
        </BarChart>
      </ResponsiveContainer>
    </MotionPaper>
  );
};

export default CollectionTrendsChart;
