import { useState } from "react";
import {
  LineChart,
  Line,
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
  ToggleButton,
  ToggleButtonGroup,
  Box,
} from "@mui/material";
import { motion } from "framer-motion";

const MotionPaper = motion(Paper);

const CollectionEfficiencyChart = ({ data }) => {
  const [timeRange, setTimeRange] = useState("all");
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
    2022:
      data["2022"]?.find((d) => d.month === idx + 1)?.promedio_eficiencia || 0,
    2023:
      data["2023"]?.find((d) => d.month === idx + 1)?.promedio_eficiencia || 0,
    2024:
      data["2024"]?.find((d) => d.month === idx + 1)?.promedio_eficiencia || 0,
    2025:
      data["2025"]?.find((d) => d.month === idx + 1)?.promedio_eficiencia || 0,
  }));

  const filteredData =
    timeRange === "all"
      ? formattedData
      : formattedData.slice(
          Math.max(formattedData.length - parseInt(timeRange), 0)
        );

  return (
    <MotionPaper
      elevation={3}
      sx={{
        p: 3,
        mb: 3,
        borderRadius: 2,
        background: "linear-gradient(145deg, #ffffff 0%, #f5f5f5 100%)",
      }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Box
        display="flex"
        justifyContent="space-between"
        alignItems="center"
        mb={2}
      >
        <Typography variant="h6" fontWeight="bold">
          Eficiencia de Cobranza por Año
        </Typography>
        <ToggleButtonGroup
          value={timeRange}
          exclusive
          onChange={(e, value) => value && setTimeRange(value)}
          size="small"
        >
          <ToggleButton value="3">3M</ToggleButton>
          <ToggleButton value="6">6M</ToggleButton>
          <ToggleButton value="all">Todo</ToggleButton>
        </ToggleButtonGroup>
      </Box>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={filteredData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
          <XAxis dataKey="month" stroke="#666" />
          <YAxis unit="%" stroke="#666" />
          <Tooltip
            contentStyle={{
              backgroundColor: "rgba(255, 255, 255, 0.9)",
              border: "none",
              borderRadius: "8px",
              boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
            }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="2022"
            stroke="#8884d8"
            strokeWidth={2}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
          />
          <Line
            type="monotone"
            dataKey="2023"
            stroke="#82ca9d"
            strokeWidth={2}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
          />
          <Line
            type="monotone"
            dataKey="2024"
            stroke="#ffc658"
            strokeWidth={2}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
          />
          <Line
            type="monotone"
            dataKey="2025"
            stroke="#ff7300"
            strokeWidth={2}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </MotionPaper>
  );
};

export default CollectionEfficiencyChart;
